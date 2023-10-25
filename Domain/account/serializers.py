from rest_framework import serializers
from Domain.account.models import User
from Domain.additionalInfo.serializers import AddressSerializer
from Domain.paiementMethod.serializers import PaiementMethodSerializer
from Domain.phone.serializers import PhoneSerializer
from Domain.reduction.serializers import ReductionSerializer
from Domain.wallet.serializers import WalletSerializer


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True, read_only=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'user_slug', 'email', 'is_active',
                  'email_confirmed', 'first_name', 'last_name', 'bio']


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

