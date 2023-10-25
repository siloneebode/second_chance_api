from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from Domain.Utils.permissions.permissions import CanDoSomething
from Domain.additionalInfo.models import Address
from Domain.additionalInfo.serializers import AddressSerializer


class AddressView(viewsets.ModelViewSet):
    http_method_names = ('post', 'get')
    permission_classes = [IsAuthenticated, CanDoSomething]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

            return JsonResponse({
                "data": serializer.validated_data,
                "message": "Address ajoutée avec success "
            }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = AddressSerializer(self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse({
            "data": serializer.validated_data,
            "message": "Address modifiée avec success "
        }, status=status.HTTP_201_CREATED)
