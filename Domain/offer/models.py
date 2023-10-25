from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from Domain.account.models import User
from Domain.product.models import Product


class Offer(models.Model):
    OFFER_TYPES = (
        ('WAITING', 'WAITING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('REFUSED', 'REFUSED'),
        ('EXPIRED', 'EXPIRED')
    )

    EXPIRED_DAY = 2

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_offers')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_offers')
    price = models.PositiveIntegerField(null=False)
    state = models.CharField(choices=OFFER_TYPES, default='WAITING', max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    # une offre expire au bout de deux jours
    expired_at = models.DateTimeField(default=(now() + timedelta(days=EXPIRED_DAY)))
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return self.expired_at < now()


class OfferChange(models.Model):
    pass

