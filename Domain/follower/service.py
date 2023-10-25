from Domain.account.models import User, Group
from Domain.follower.models import Follow


def follow_service(request, kwargs):
    seller = User.objects.get(pk=kwargs['pk'], user_slug=kwargs['slug'])
    # TODO: On doit regarder ici si personne n'a bloqué l'autre.
    follow = Follow.objects.create(user=request.user, seller=seller)
    group = Group(name=request.user.channels['private'])
    group.save()
    request.user.add(group)
    follow.save()
    # TODO: SI le vendeur a activé ce type de notification
    return follow


def send_private_notification():
    pass
