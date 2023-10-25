import uuid as uuid
from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from Domain.account.models import User
from Domain.deliverySetting.models import Delivery
from Domain.paiementMethod.models import PaiementMethod
from Domain.product.models import Product


class Order(models.Model):
    ORDER_STATES = (
        ('WAITING', 'en attente'),
        ('ACCEPTED', 'acceptée'),
        ('REFUSED', 'refusée'),
        ('CANCELED', 'annulée'),
        ('SUSPENDED', 'suspendu'),
        ('REFUNDED', 'remboursée'),
        ('FINISHED', 'terminée'),
        ('DELIVERING', 'en cours de livraison '),
        ('DELIVERED', 'livré'),
        ('VERIFIED', 'vérifié'),

    )

    TIME_TO_ACCEPT = 1
    CLIENT_OK_TIME = 3
    DISTANCE_FOR_VERIFICATION = 50
    TIME_FOR_SELLER_AFTER_ACCEPTED = 1
    TIME_FOR_DELIVERY_TO_SHIP = 2
    TIME_FOR_CLIENT_TO_CONFIRM_AFTER_SHIP = 48
    ORDER_EXPIRED_TIME = 5

    ref = models.CharField(null=True, max_length=255)
    price = models.FloatField(null=True)
    method = models.ForeignKey(PaiementMethod, on_delete=models.PROTECT, default=None)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, default=None)
    first_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    city = models.CharField(null=True, max_length=255)
    street = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=255)
    has_verification = models.BooleanField(default=False)
    fee = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    seller_accept_order_expired_at = models.DateTimeField(default=(now() + timedelta(days=TIME_TO_ACCEPT)))
    client_confirm_ok_expired_at = models.DateTimeField(null=True)
    order_expired_at = models.DateTimeField(default=(now() + timedelta(days=ORDER_EXPIRED_TIME)))

    # SI LE CLIENT ET LE VENDEUR SE GÈRENT
    client_confirm_receive_expired_at = models.DateTimeField(null=True)

    # SI LE CLIENT PAYE UNE LIVRAISON SUR LE SITE.
    seller_ship_to_deliver_expired_at = models.DateTimeField(null=True)
    deliver_ship_expired_at = models.DateTimeField(null=True)

    # SI LE CLIENT A PAYÉ POUR UNE VÉRIFICATION.
    client_ok_time_expired_at = models.DateTimeField(null=True)
    state = models.CharField(choices=ORDER_STATES, default='WAITING', max_length=25)

    @property
    def can_accept_order(self):
        return self.seller_accept_order_expired_at > now()


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('PURCHASE', 'Achat'),
        ('SALE', 'vente'),
        ('REFUND', 'remboursement'),

    )
    price = models.FloatField(null=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, default=None)
    method = models.ForeignKey(PaiementMethod, on_delete=models.PROTECT, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    method_ref = models.CharField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)
    city = models.CharField(null=True, max_length=255)
    street = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=255)
    fee = models.FloatField(default=0)
    type = models.CharField(choices=TRANSACTION_TYPES, default='PURCHASE', max_length=20)
