from rest_framework import serializers

from Domain.additionalInfo.models import Address, UserLoginIp


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'street', 'city', 'title', 'id', 'for_delivery']

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)
        return address

    def update(self, instance, validated_data):
        return instance.save(**validated_data)


class UserLoginIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginIp
        fields = ['name', 'owner']
