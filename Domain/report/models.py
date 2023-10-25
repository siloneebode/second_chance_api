from django.db import models

from Domain.account.models import User
from Domain.product.models import Product
from Domain.review.models import Review, ReviewReply


class UserReport(models.Model):
    REPORT_RAISONS = (
        ('SWINDLER', 'Le vendeur est un arnaqueur'),
        ('BAD_PROMOTION', 'Le vendeur a un ou plusieurs produits volés'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    raison = models.CharField(choices=REPORT_RAISONS, default='SWINDLER', max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ReviewReport(models.Model):
    REPORTS_RAISONS = (
        ('INSULTANT', 'Contenu insultant'),
        ('MENSONGER', 'Contenu mensonger'),
        ('ERROR', 'Cette personne n\'a pas le droit de me mettre une note'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review_reports')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    raison = models.CharField(choices=REPORTS_RAISONS, default='INSULTANT', max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ReviewReplyReport(models.Model):
    REPLY_RAISONS = (
        ('INSULTANT', 'Contenu insultant'),
        ('MENSONGER', 'Contenu mensonger'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review_reply_reports')
    reply = models.ForeignKey(ReviewReply, on_delete=models.CASCADE)
    raison = models.CharField(choices=REPLY_RAISONS, default='INSULTANT', max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductReport(models.Model):
    REPORT_RAISONS = (
        ('FAKE', 'Le produit n\'existe pas'),
        ('INFRINGEMENT', 'Produit contrefait'),
        ('STOLEN', 'Produit volé'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reports')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raison = models.CharField(choices=REPORT_RAISONS, default='STOLEN', max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
