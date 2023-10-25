from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ['id', 'price', 'price_waiting', 'active']

    def update(self, instance, validated_data):
        instance.active = True
        instance.price = 0
        instance.price = 0
        instance.save()
        return instance
