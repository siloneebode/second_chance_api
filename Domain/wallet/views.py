from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, serializers, status

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.Utils.permissions.permissions import CanActivateWallet
from Domain.phone.models import Phone
from Domain.wallet.models import Wallet
from Domain.wallet.serializers import WalletSerializer


class WalletView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [CanActivateWallet]

    def get_queryset(self):
        return Wallet.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        wallet = Wallet.objects.filter(token=kwargs['token'])
        if wallet.exists():
            serializer = self.serializer_class(wallet).data
        else:
            raise serializers.ValidationError({"message": "erreur inconnue... "})

        return JsonResponse(
            {'message': "Tu as activé ton portemonnaie virtuel avec success, "
                        "Chaque fois que fera une vente, le montant sera crédité dans ton portemonnaie ",
             'data': serializer.data

             }, status=status.HTTP_200_OK)
