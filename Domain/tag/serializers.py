from rest_framework import serializers

from Domain.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)
