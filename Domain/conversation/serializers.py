from rest_framework import serializers

from Domain.conversation.models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['sticky', 'id', 'author', 'receiver', 'admin']
