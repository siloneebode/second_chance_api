from django.db import models

from Domain.account.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
