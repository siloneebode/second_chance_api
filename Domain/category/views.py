from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework import serializers
from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.category.models import Category, SubCategory, EndCategory
from Domain.category.serializers import CategorySerializer, SubCategorySerializer, EndCategorySerializer


class CategoryListView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = []
    lookup_fields = ['category_slug']

    def get_queryset(self):
        return Category.objects.filter(active=True)

    @action(['GET'], detail=True)
    def get_category(self, request, *args, **kwargs):
        serializer = CategorySerializer(self.get_object(), many=False)
        if serializer.data:
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse({"message": "erreur Inconnu... Veuillez réessayer..."}, status=status.HTTP_200_OK)


class SubCategoryView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = []
    lookup_fields = ['category_slug', 'sub_category_slug']

    def get_queryset(self):
        queryset = SubCategory.objects.filter(active=True)
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    @action(['GET'], detail=True)
    def get_sub_category(self, request, *args, **kwargs):
        try:
            sub_category = SubCategory.objects.get(sub_category_slug=kwargs['sub_category_slug'])
            serializer = SubCategorySerializer(sub_category)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({'message': 'Impossible de charger la sous catégorie '})
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class EndCategoryView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = EndCategorySerializer
    permission_classes = []
    lookup_fields = ['sub_category_slug', 'end_category_slug']

    def get_queryset(self):
        queryset = EndCategory.objects.filter(active=True)
        sub_category_id = self.request.query_params.get('sub_category')
        if sub_category_id is not None:
            queryset = queryset.filter(sub_category_id=sub_category_id)

        return queryset

    @action(['GET'], detail=True)
    def get_end_category(self, request, *args, **kwargs):
        try:
            end_category = EndCategory.objects.get(end_category_slug=kwargs['end_category_slug'])
            serializer = EndCategorySerializer(end_category)
        except EndCategory.DoesNotExist:
            raise serializers.ValidationError({'message': 'Impossible de charger la sous catégorie '})
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
