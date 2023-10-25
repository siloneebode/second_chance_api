from rest_framework import serializers

from Domain.account.serializers import UserSerializer
from Domain.product.serializers import ProductSerializer
from Domain.report.models import UserReport, ProductReport, ReviewReport, ReviewReplyReport
from Domain.review.serializers import ReviewSerializer


class UserReportSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()

    class Meta:
        model = UserReport
        fields = ['owner', 'seller', 'id']

    def get_owner(self, obj):
        return obj.owner.id

    def get_seller(self, obj):
        return obj.seller.id

    def create(self, validated_data):
        report = UserReport.objects.create(raison=validated_data['raison'])
        return report.save()


class ProductReportSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = ProductReport
        fields = ['owner', 'product', 'raison']

    def create(self, validated_data):
        report = ProductReport.objects.create(raison=validated_data['raison'])
        return report.save()


class ReviewReportSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    review = ReviewSerializer()

    class Meta:
        model = ReviewReport
        fields = ['owner', 'review', 'active']

    def create(self, validated_data):
        report = ReviewReport.objects.create(raison=validated_data['raison'])
        return report.save()


class ReviewReplyReportSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    reply = ReviewSerializer()

    class Meta:
        model = ReviewReplyReport
        fields = ['owner', 'reply', 'active', 'raison']

    def create(self, validated_data):
        report = ReviewReplyReport.objects.create(raison=validated_data['raison'])
        return report.save()
