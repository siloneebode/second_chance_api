from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.conversation.models import Conversation
from Domain.conversation.serializers import ConversationSerializer


class ConversationView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(author=self.request.user)


