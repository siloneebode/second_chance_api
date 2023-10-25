from django.db import models

from Domain.account.models import User
from Domain.conversation.models import Conversation


class Message(models.Model):
    TYPES = (
        ("TEXT", "TEXT"),
        ("IMAGE", "IMAGE")
    )
    content = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    image = models.ImageField(null=True)
    type = models.CharField(choices=TYPES, default='TEXT', null=False, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
