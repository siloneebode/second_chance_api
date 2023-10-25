from django.db.models.signals import post_save
from django.dispatch import receiver
from Domain.account.models import User, Group
from Domain.follower.models import Follow


# Le signal se déclenche quand un EmailVerification object vient d'etre sauvegardé
@receiver(post_save, sender=Follow)
def notify_user(sender, instance, created, **kwargs):
    add_user_to_group(instance)


# methode qui ajoute le canal public du vendeur parmi les canaux du user.
def add_user_to_group(instance):
    seller_public = instance.seller.channels()[1]
    group = Group(name=seller_public)
    group.save()
    group.owners.add(instance.user)
    group.save()
