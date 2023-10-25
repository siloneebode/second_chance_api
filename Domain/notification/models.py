from django.db import models

from Domain.account.models import User

# LES TYPES DE NOTIFICATION
NOTIFICATIONS_TYPES = (
    ('NEW_FOLLOWER', 'NEW_FOLLOWER'),
    ('NEW_OFFER', 'NEW_OFFER'),
    ('NEW_FEATURE', 'NEW_FEATURE'),
    ('OFFER_UPDATED', 'OFFER_UPDATED'),
    ('NEW_ORDER', 'NEW_ORDER'),
    ('NEW_PRODUCT', 'NEW_PRODUCT'),
    ('NEW_EVALUATION', 'NEW_EVALUATION'),
    ('MARKETING_OFFER', 'MARKETING_OFFER'),
    ('FAVORIS_ADD', 'FAVORIS_ADD')
)


class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(null=False, max_length=255)
    title = models.CharField(null=False, max_length=255)
    url = models.CharField(null=True, max_length=255)
    target = models.CharField(null=True, max_length=255)
    group = models.CharField(default='public', null=False, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=25, null=False, choices=NOTIFICATIONS_TYPES, default='NEW_FEATURE')
    image = models.IntegerField(default=None)
