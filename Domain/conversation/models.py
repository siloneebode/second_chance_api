from django.db import models
from Domain.account.models import User


class Conversation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    sticky = models.BooleanField(default=0, null=False, max_length=255)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation')
    # last_message = models.ForeignKey(Message, on_delete=models.PROTECT, null=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='litiges', null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # TODO: Dès qu'on récupère le model produit sur github on ajoute ca ici.
    #  une conversation peut ou pas être liée à un produit.


class ConversationReadTime(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='readtimes')
    read_at = models.DateTimeField(auto_now_add=True)
