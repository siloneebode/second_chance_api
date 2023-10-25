import uuid

from django.db import models

from Domain.account.models import User


class Wallet(models.Model):
    token = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    price = models.FloatField(null=True)
    price_waiting = models.FloatField(null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class WalletTransaction(models.Model):
    pass
