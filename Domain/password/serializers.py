from rest_framework import serializers
from Domain.account.models import User
from Domain.password.models import PasswordReset
import re

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = PasswordReset
        fields = ['email']

    def validate(self, data):

        if User.objects.filter(email=data['email'], is_active=True).exists():
            return data
        else:
            raise serializers.ValidationError("Erreur, utilisateur inconnu ou compte bloqué.")

    def create(self, validated_data):
        return PasswordReset.objects.create(**validated_data)


class UpdatePasswordSerializer(serializers.ModelSerializer):
    first_password = serializers.CharField(write_only=True, required=True)
    second_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_password', 'second_password', 'password']

    # validateur de mot de passe. Pour plus de précision on peut écrire notre propre validateur.
    def validate(self, attrs):

        if attrs['first_password'] != attrs['second_password']:
            raise serializers.ValidationError("Les mots de passe ne concordent pas")

        regex = re.compile(r'^(?=.*[A-Z])(?=.*d)(?=.*[!@#$%^&*()_+])[A-Za-zd!@#$%^&*()_+]{6,}$')

        if regex.match(attrs['first_password']):
            return attrs
        else:
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins une majuscule, au moins un chiffre,"
                " au moins un caractère spécial et au moins 6 caractères.")

    def update(self, instance, validated_data):
        instance.set_password(validated_data['first_password'])
        instance.save()
        return instance
