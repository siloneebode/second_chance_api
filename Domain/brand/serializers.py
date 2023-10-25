from rest_framework import serializers
from Domain.brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'brand_slug']
        lookup_field = 'brand_slug'
