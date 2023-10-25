from rest_framework import serializers

from Domain.paiementMethod.models import PaiementMethod


class PaiementMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaiementMethod
        fields = ['method', 'image', 'id']
