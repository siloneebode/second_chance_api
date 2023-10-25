from django.db import models

from Domain.account.models import User


# représente une adresse ip d'un utilisateur
class UserLoginIp(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ip = models.GenericIPAddressField(null=False)
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    title = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    country = models.CharField(null=False, max_length=255)
    first_name = models.CharField(null=False, max_length=255, default=None)
    last_name = models.CharField(null=False, max_length=255, default=None)
    street = models.CharField(null=True, max_length=255, default=None)
    city = models.CharField(null=False, max_length=255, default=None)
    for_delivery = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class IdentityCard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='identity_card')
    type = models.CharField(null=False, max_length=255)
    recto = models.ImageField(null=False)
    verso = models.ImageField(null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


# model qui représente un ip bloqué en base de donnée
class IpBlocked(models.Model):
    ip = models.GenericIPAddressField(null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ip')
