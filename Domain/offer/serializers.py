from django.utils.timezone import now
from rest_framework import serializers

from Domain.offer.models import Offer
from Domain.product.models import Product


class OfferSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('id', 'price', 'state', 'state')

    def get_expired(self, obj):
        return obj.expired_at > now()

