from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Domain.account.models import User
from Domain.review.models import Review
from Domain.review.serializers import ReviewSerializer


class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        seller = User.objects.get(pk=self.kwargs['seller'])
        serializer.save(owner=self.request.user, seller=seller)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pass

