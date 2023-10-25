from django.utils.text import slugify
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Domain.account.models import User
from Domain.account.serializers import UserSerializer
from Domain.auth.models import EmailVerification


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'id', 'is_active', 'email_confirmed']
        read_only_field = ['is_active', 'email_confirmed']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.user_slug = slugify(validated_data['username'])

        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.banned_at and self.user.banned_at > now():
            raise serializers.ValidationError({"Votre compte est bloqué."})
        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class EmailVerificationSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = EmailVerification
        fields = ['token', 'user_id', 'username']

    def get_user_id(self, obj):
        return obj.author.id

    def get_username(self, obj):
        return obj.author.username

    def create(self, validated_data):
        pass

