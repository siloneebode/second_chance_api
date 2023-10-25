from rest_framework import serializers

from Domain.account.serializers import UserSerializer
from Domain.review.models import Review, ReviewReply


class ReviewSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    seller = UserSerializer()

    class Meta:
        model = Review
        fields = ['owner', 'seller', 'content', 'active']


class ReviewReplySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    review = ReviewSerializer()

    class Meta:
        model = ReviewReply
        fields = ['owner', 'review', 'content', 'active']
