from django.db import models

from Domain.account.models import User


class Delivery(models.Model):

    DELIVERY_TITLES = (
        ('TITLE_1', 'livraison par le vendeur'),
        ('TITLE_2', 'récupération chez le livreur'),
        ('TITLE_3', 'livraison gratuite du vendeur')
    )

    price = models.FloatField(null=False, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(choices=DELIVERY_TITLES, default='TITLE_1', max_length=255)
    content = models.TextField(null=False)
    active = models.BooleanField(default=True)

