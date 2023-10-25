from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.brand.models import Brand
from Domain.brand.serializers import BrandSerializer
from Domain.product.models import Product


class BrandView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    permission_classes = []
    lookup_fields = ['brand_slug']

    def get_queryset(self):
        return Brand.objects.filter(active=True)

    def get_product_by_brand(self):
        return Product.objects.filter(brand=self.name)

    @action(['GET'], detail=True)
    def get_brand(self, request, *args, **kwargs):
        serializer = BrandSerializer(self.get_object(), many=False)
        if serializer.data:
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({"message": "erreur Inconnu..."}, status=status.HTTP_200_OK)
