from rest_framework import serializers
from Domain.account.serializers import UserSerializer
from Domain.product.models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = ["id", "title", "price", "images"]

    def get_image(self, obj):
        return ProductImage.objects.get(product=obj, default=True)

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images')
        instance.save(**validated_data)

        return instance, images

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductDetailSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer()
    owner = UserSerializer()

    class Meta:
        model = Product
        fields = ["id", "title", "price",
                  "images", "content", "category",
                  "brand", "owner", "reserved"]


