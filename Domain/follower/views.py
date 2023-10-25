from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.account.models import User, Group
from Domain.follower.models import Follow
from Domain.follower.serializes import FollowSerializer
from Domain.follower.service import follow_service
from Domain.services import send_channel_notification


class FollowView(viewsets.ModelViewSet, MultipleFieldLookupMixin):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = ['id', 'slug']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # je récupère le vendeur depuis la requête à l'aide du get_object() de la mixin dont hérite ma vue.
        seller = User.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        # je récupère l'utilisateur actuellement connecté avec le self.request.user
        # et je sauvegarde le follow entity avec les params
        serializer.save(user=user, seller=seller)
        send_channel_notification(
            channel='private' + user.id,
            type_of="notification_follower",
            target=user
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

            return JsonResponse({
                'data': serializer.data,
                'message': "Tu suis désormais ce vendeur. "
                           "Tu seras notifié quand le vendeur ajoutera un nouvel article en vente"
            }, status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, *args, **kwargs):

        try:
            follow = follow_service(request, kwargs)

        except Follow.DoesNotExist:
            raise serializers.ValidationError({
                "message": "Erreur lors de l'abonnement à ce vendeur, réessayez plus tard "})

        return JsonResponse({
            'data': FollowSerializer(follow).data,
            'message': "Tu suis désormais ce vendeur. "
                       "Tu seras notifié quand le vendeur ajoutera un nouvel article en vente"
        }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        if serializer.is_valid(raise_exception=True):
            return JsonResponse({
                'message': 'Tu ne suis plus ce vendeur. '
            })
