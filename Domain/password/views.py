from django.http.response import JsonResponse
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.account.models import User
from Domain.password.models import PasswordReset
from Domain.password.serializers import PasswordResetSerializer, UpdatePasswordSerializer


class PasswordResetView(viewsets.ModelViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

            return JsonResponse({
                'message': "Demande de réinitialisation envoyée, va dans ton email pour changer de mot de passe. "
            }, status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def confirm_reset(self, request, token):
        token = PasswordReset.objects.filter(token=token).get()
        if token.expired_at < now():
            token.delete()
            return JsonResponse(
                {"data": "Erreur Token invalide ou expiré, veuillez refaire une demande de réinitialisation"})

        return JsonResponse({"data": "Redirection..."})


class ChangeResetPasswordView(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = UpdatePasswordSerializer

    def get_queryset(self):
        return User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())

        return JsonResponse({
            'data': serializer.data,
            'message': "mot de passe réinitialisé avec success."
        }, status=status.HTTP_200_OK)
