from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Domain.account.models import User
from Domain.account.serializers import UserSerializer, UserUpdateSerializer
from Domain.auth.serializers import RegisterSerializer


class UserDetailsView(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserUpdateView(viewsets.ModelViewSet):
    serializer_class = UserUpdateSerializer

    permission_classes = (IsAuthenticated,)
    http_method_names = ['post']

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def update(self, request, *args, **kwargs):
        user = self.get_queryset().get(pk=kwargs['pk'])
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
















