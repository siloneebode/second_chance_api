from rest_framework import serializers

from Domain.message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'author', 'type', 'image']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
