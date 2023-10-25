import uuid
from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from Domain.account.models import User


class EmailVerification(models.Model):
    token = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=False)

    @property
    def is_expired(self):
        return self.expired_at > now()



