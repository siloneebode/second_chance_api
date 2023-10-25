from django.db import models

from Domain.account.models import User


class Reduction(models.Model):
    nbr_products = models.PositiveIntegerField(null=False)
    percent = models.FloatField(max_length=255, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
