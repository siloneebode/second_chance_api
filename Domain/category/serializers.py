from rest_framework import serializers

from Domain.category.models import Category, SubCategory, EndCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_slug']


class SubCategorySerializer(serializers.ModelSerializer):
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'sub_category_slug', 'category', 'category_slug')

    def get_category_slug(self, obj):
        return obj.category.category_slug


class EndCategorySerializer(serializers.ModelSerializer):
    sub_category_slug = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = EndCategory
        fields = ('id', 'name', 'sub_category', 'category_slug', 'sub_category_slug', 'end_category_slug')

    def get_category_slug(self, obj):
        return obj.sub_category.category.category_slug

    def get_sub_category_slug(self, obj):
        return obj.sub_category.sub_category_slug
