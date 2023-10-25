from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from Domain.account.models import User


class Phone(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    phone = models.CharField(null=False, max_length=255)
    country = models.CharField(null=False, max_length=255)
    is_verified = models.BooleanField(default=False)
    for_paiement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class PhoneVerification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(null=False, max_length=255)
    token = models.CharField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(default=(now() + timedelta(hours=1)))
