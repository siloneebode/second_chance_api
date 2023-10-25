from django.db import models


class PaiementMethod(models.Model):
    PAIEMENT_METHODS = (
        ('WALLET', 'mon portemonnaie'),
        ('OM', 'Orange money'),
        ('MOMO', 'Mtn money'),
        ('MIXED', 'mixte')

    )

    method = models.CharField(choices=PAIEMENT_METHODS, default='WALLET', max_length=10)
    fee = models.FloatField(null=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
