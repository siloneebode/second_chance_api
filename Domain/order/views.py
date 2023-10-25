import uuid
from datetime import timedelta

from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.Utils.permissions.permissions import CanCreateOrder, CanManageOrder
from Domain.deliverySetting.models import Delivery
from Domain.order.models import Order
from Domain.order.serializers import OrderSerializer
from Domain.order.services import create_order
from Domain.paiementMethod.models import PaiementMethod
from Domain.product.models import Product
from Domain.wallet.models import Wallet


class OrderView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CanCreateOrder]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['product'])
        # TODO: Pour le moment on gère avec le wallet
        wallet = Wallet.objects.get(owner=self.request.user)
        seller = product.owner

        # on récupère la méthode de paiement depuis les data
        method = PaiementMethod.objects.get(pk=self.request.data['method'])

        # on récupère la méthode de livraison choisie par le client.
        delivery = Delivery.objects.get(pk=self.request.data['delivery'])

        # on vérifie si le portemonnaie du client a suffisamment de fonds pour effectuer l'achat.
        if wallet.price >= product.price:

            # si oui on sauvegarde la commande.
            serializer.save(
                product=product,
                price=(product.price + delivery.price),
                ref=(str(uuid.uuid4()).split("-")[0]).upper(),
                buyer=self.request.user,
                fee=15,
                has_verification=False,
                delivery=delivery,
                method=method,
                first_name=self.request.data['first_name'],
                last_name=self.request.data['last_name'],
                street=self.request.data['street'],
                city=self.request.data['city'],
                phone=self.request.data['phone'],
            )

            # on incrémente son nombre de produit vendu
            product.owner.total_sold = product.owner.total_sold + 1
            product.owner.save()

            # je marque le produit comme vendu
            product.is_sold = True
            product.save()

        else:
            raise serializers.ValidationError({"message": "Vous n'avez pas suffisamment de fond pour acheter. "})

    @action(['POST'], detail=True, permission_classes=[IsAuthenticated, CanCreateOrder])
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = create_order(request.data, kwargs, request)
            return JsonResponse({'data': response},
                                status=status.HTTP_201_CREATED)
        return JsonResponse({'message': "Erreur lors de l'initiation du paiement "},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(['GET'], detail=True)
    def callback(self, request, *args, **kwargs):

        # on attend la réponse de l'api puis on recupère les données.
        data = request.data
        ref = data['transaction_ref']
        if data['transaction_status'] == 'SUCCESS':
            pass
            # TODO: Paiement bien passé
            product = Product.objects.get(pk=data['app_transaction_ref'].split('.'[1]))
            product.is_sold = True
            product.save()
            # TODO: Je notifie le vendeur qu'il vient d'avoir une nouvelle commande.
        else:
            # Paiement échoué
            Order.objects.filter(ref=ref).delete()
            # TODO: J'envoie le mail au client que son achat n'est pas passé.

    @action(['POST'], detail=True, permission_classes=[CanManageOrder])
    def accept_order(self, request, *args, **kwargs):
        CLIENT_OK_TIME = 3
        TIME_FOR_SELLER_AFTER_ACCEPTED = 1

        order = Order.objects.get(pk=kwargs['pk'])
        if order is None:
            raise NotFound('Erreur, commande introuvable')
        if order.state != 'WAITING':
            raise PermissionDenied('Erreur inconnue, veuillez réessayer...')
        if order.seller_accept_order_expired_at < now():
            raise PermissionDenied('Erreur, La commande a deja expirée...')
        with transaction.atomic():
            order.state = 'ACCEPTED'
            delivery = Delivery.objects.get(pk=order.delivery.pk)
            if delivery.owner == request.user:
                order.client_confirm_ok_expired_at = now() + timedelta(days=CLIENT_OK_TIME)
            else:
                order.seller_ship_to_deliver_expired_at = now() + timedelta(days=TIME_FOR_SELLER_AFTER_ACCEPTED)
            order.save()
        # TODO: On notifie le client que son offre viens d'etre acceptée avec success
        return JsonResponse(
            {'message': "Tu as accepté la commande, tu recevras un mail qui t'indiquera la marche à suivre. "})

    @action(['POST'], detail=True, permission_classes=[CanManageOrder])
    def refuse_order(self, request, *args, **kwargs):
        CLIENT_OK_TIME = 3
        TIME_FOR_SELLER_AFTER_ACCEPTED = 1

        order = Order.objects.get(pk=kwargs['pk'])
        if order is None:
            raise NotFound('Erreur, commande introuvable')
        if not order.can_accept_order():
            raise PermissionDenied('La commande a deja expirée...')
        if order.state == 'WAITING':
            with transaction.atomic():
                order.state = 'REFUSED'
                order.save()
        # TODO: On notifie le client que son offre viens d'etre acceptée avec success
        return JsonResponse(
            {'message': "Tu as refusé la commande, l'acheteur sera notifié de ton refus."})

    def create_litige(self, request, *args, **kwargs):
        pass


