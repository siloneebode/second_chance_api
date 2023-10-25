from django.db import models

from Domain.account.models import User
from Domain.order.models import Order


class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_reviews')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    is_parent = models.BooleanField(default=True)
    rate = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ReviewReply(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reply')
    active = models.BooleanField(default=True)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)



