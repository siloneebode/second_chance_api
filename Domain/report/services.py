from rest_framework.exceptions import PermissionDenied

from Domain.review.models import Review, ReviewReply


def create_review_report(serializer, user, kwargs):
    review = Review.objects.get(active=True, pk=kwargs['review'], is_parent=True)
    # on vérifie si le current user est le vendeur du produit du départ sinon on renvoie une exception.
    if review is not None and review.order.product.owner == user:
        serializer.save(owner=user, review=review)
    else:
        raise PermissionDenied("Erreur, l'avis est introuvable. ou tu n'as pas la permission de supprimer cette avis ")


def create_reply_report(serializer, user, kwargs):
    reply = ReviewReply.objects.get(active=True, pk=kwargs['reply'])
    # on vérifie si le current user est l'acheteur du produit du départ sinon on renvoie une exception.
    if reply is not None and reply.order.buyer == user:
        serializer.save(owner=user, reply=reply)
    else:
        raise PermissionDenied("Erreur, l'avis est introuvable. ou tu n'as pas la permission de supprimer cette avis ")
