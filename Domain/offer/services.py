from django.http.response import JsonResponse
from rest_framework import serializers, status

from Domain.offer.models import Offer
from Domain.product.models import Product


def create_offer(request, kwargs):
    product = Product.objects.filter(pk=kwargs['product'])
    if product.exists() and product.get().is_sold == False:
        offer = Offer.objects.filter(owner=request.user, product=kwargs['product'],
                                     state='WAITING') | Offer.objects.filter(owner=request.user,
                                                                             product=kwargs['product'],
                                                                             state='ACCEPTED')
        if offer.exists() and offer.get().state == 'WAITING':
            raise serializers.ValidationError({'message': "Tu as deja une offre en attente"})
        if offer.exists() and offer.get().state == 'ACCEPTED':
            raise serializers.ValidationError({'message': "Le vendeur a deja accepté ton offre. Vite passe à "
                                                          "l'achat"})
    else:
        raise serializers.ValidationError({'message': "Produit introuvable ou article deja vendu.."})


def manage_offer(offer, action):
    if offer.is_expired:
        raise serializers.ValidationError({"message": "Erreur, l'offre du client est deja expirée"})
    if offer.state == 'ACCEPTED':
        raise serializers.ValidationError({"message": "Vous avez deja accepté l'offre. "})
    try:
        if action == "accept":
            if offer.state == 'WAITING':
                offer.state = 'ACCEPTED'
                offer.save()
                # TODO: On doit envoyer une notification ici au client que son offre a été refusée qu'il peut désormais payer.
                return JsonResponse({'message': 'Tu as accepté l\'offre, passe maintenant à l\'achat.'})
        elif action == "refuse":
            if offer.state == 'REFUSED':
                raise serializers.ValidationError({"message": "Vous avez deja refusé cette offre. "})
            if offer.state == 'WAITING':
                offer.state = 'REFUSED'
                offer.save()
                # TODO: On doit envoyer une notification ici au client que son offre a été refusée qu'il peut désormais payer.
                return JsonResponse({'message': 'Tu as refusé l\'offre '})
        else:
            return JsonResponse({'message': 'Erreur inconnue, veuillez réessayer...'},
                                status=status.HTTP_401_UNAUTHORIZED)

    except Offer.DoesNotExist:
        raise serializers.ValidationError({'message': 'Erreur inconnue...'})
