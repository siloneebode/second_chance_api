import uuid
from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from Domain.account.models import User


class PasswordReset(models.Model):
    token = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=(now() + timedelta(minutes=30)))
