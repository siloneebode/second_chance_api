from django.utils.timezone import now
from rest_framework import serializers

from Domain.reduction.models import Reduction


class ReductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reduction
        fields = ['id', 'nbr_product', 'percent', 'active']

    def create(self, validated_data):
        return Reduction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nbr_product = validated_data.get('nbr_product', instance.nbr_product)
        instance.percent = validated_data.get('percent', instance.percent)
        instance.updated_at = now()

        instance.save()
        return instance
