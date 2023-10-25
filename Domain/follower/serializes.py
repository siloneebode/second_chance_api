from rest_framework import serializers

from Domain.follower.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['active']

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.active = False
        instance.save()
        return instance


