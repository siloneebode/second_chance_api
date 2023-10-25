from django.db import models

from Domain.account.models import User
from Domain.product.models import Product


class Favoris(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes_count')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

