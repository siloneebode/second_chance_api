from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action

from Domain.Utils.permissions.permissions import CanManageOffer
from Domain.account.models import User
from Domain.offer.models import Offer
from Domain.offer.serializers import OfferSerializer
from Domain.offer.services import create_offer, manage_offer
from Domain.product.models import Product


class OfferView(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [CanManageOffer]

    def get_queryset(self):
        return Offer.objects.filter(owner=self.request.user) | Offer.objects.filter(
            seller=self.kwargs['seller'])

    def perform_create(self, serializer):
        seller = User.objects.get(pk=self.kwargs['seller'])
        product = Product.objects.get(pk=self.kwargs['product'])

        if product:
            with transaction.atomic():
                create_offer(self.request, product)
                serializer.save(seller=seller, owner=self.request.user, product=product)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse({"message": "offre envoyée avec succès, "
                                        "le vendeur doit confirmer pour que vous passsez au paiement",
                             'data': serializer.data},
                            status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True, permission_classes=[CanManageOffer])
    def accept(self, request, *args, **kwargs):
        action = request.POST.get('action')
        offer = Offer.objects.get(pk=kwargs['pk'])
        if offer and offer.seller != request.user or offer.product.owner != request.user:
            raise serializers.ValidationError({"message": "Erreur, inconnue... Vous avez usurpez ce compte..."})

        with transaction.atomic():
            manage_offer(offer, action)


