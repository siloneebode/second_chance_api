from django.utils.timezone import now
from rest_framework import serializers

from Domain.phone.models import Phone


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['phone', 'is_verified']

    def create(self, validated_data):
        phone = Phone.objects.create(**validated_data)
        phone.save()
        return phone

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.country = validated_data.get('country', instance.country)
        instance.updated_at = now()
        if instance.phone != validated_data.get('phone', instance.phone):
            instance.is_verified = False

        instance.save()
        return instance
