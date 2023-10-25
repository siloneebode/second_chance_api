from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Domain.notification.models import Notification, NOTIFICATIONS_TYPES


# retourne tous les channels auquels peut s'abonner un utilisateur.
def get_user_channels(user):
    channels = [
        'private-' + user.id,
    ]
    user_channels = user.group_set.all()
    for channel in user_channels:
        channels.append(channel.name)

    if user.is_superuser:
        channels.append('admin')

    return channels


# service qui permet d'envoyer des notifications à un channel
# on se servira de ce cannal pour envoyer des notifications push
def send_channel_notification(channel, type_of, target=None):
    notification = Notification(

    )
    if type_of == "notification_offer":
        # url sera l'url de la conversation entre les deux.
        notification.url = 'tuto'

    if type_of == "notification_follower":
        notification.title = "Nouveau follower"
        notification.message = target.username + "vient de s'abonner à ton compte. "
        notification.url = None
        notification.image = None
        notification.group = 'private-' + target.id,
        notification.type = "NEW_FOLLOWER"
        notification.save()
    if type_of == "notification_product":
        notification.url = "url de la page détail du produit."

    if type_of == "notification_price":
        notification.url = "url de la page détail du produit."
    if type_of == "notification_other":
        # notification qui signale au client qui a liké un produit qu'un client vient de faire une offre sur ce produit.
        notification.url = "url du produit en question" \
                           " ou url de la conversation entre elle et le vendeur "

    if type_of == "notification_product_sold":
        notification.url = None
        # le titre sera : le produit xx que tu as mis en favoris vient d'être acheté.

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel,
        {
            "type": type_of,
            "data": notification
        }
    )


def send_push_notification():
    pass


def send_user_notification(user):
    pass
