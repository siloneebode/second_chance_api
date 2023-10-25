from rest_framework import serializers

from Domain.order.models import Order, Transaction
from Domain.product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    method = serializers.SerializerMethodField()
    delivery = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'price', 'ref', 'created_at', 'state', 'method', 'delivery']

    def get_method(self, obj):
        return obj.method.id

    def get_delivery(self, obj):
        return obj.delivery.id

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'price', 'product', 'created_at', 'has_verification')


class TransactionSerializer(serializers.ModelSerializer):
    product_title = serializers.SerializerMethodField()
    method_image = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'price', 'created_at', 'product_title', 'type', 'method', 'delivery']

    def get_product_title(self, obj):
        return obj.product.title

    def get_method_image(self, obj):
        return obj.method.image


class TransactionDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'price', 'created_at', 'product', 'method', 'delivery']
