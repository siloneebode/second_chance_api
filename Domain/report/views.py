from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from Domain.order.models import Order
from Domain.product.models import Product
from Domain.report.models import UserReport, ProductReport, ReviewReport, ReviewReplyReport
from Domain.report.serializers import UserReportSerializer, ProductReportSerializer, ReviewReportSerializer, \
    ReviewReplyReportSerializer
from Domain.report.services import create_review_report, create_reply_report
from Domain.review.models import Review


class UserReportView(viewsets.ModelViewSet):
    serializer_class = UserReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserReport.objects.filter(active=True, owner=self.request.user) | \
            UserReport.objects.filter(active=True, seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, seller=self.kwargs['seller'])

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = Order.objects.get(buyer=request.user, product__owner_id=kwargs['seller']) | \
                    Order.objects.get(buyer=kwargs['seller'], product__owner_id=request.user)

            # on verifie avant le blocage qu'il ny' a pas de commande en cours qui les lient.
            if order is not None and order.order_expired_at >= now():
                self.perform_create(serializer)
            else:
                raise PermissionDenied('Vous ne pouvez pas bloquer un utilisateur '
                                       'avec qui vous avez une commande en cours.')

            # TODO: Envoyer un mail au deux personnes.
        return JsonResponse({
            'data': serializer.data,
            'message': "Tu as bloqué l'utilisateur. Tu ne pourra plus rien voir de cette utilisateur. "},
            status=status.HTTP_201_CREATED)


class ProductReportView(viewsets.ModelViewSet):
    serializer_class = ProductReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductReport.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs['product'], is_sold=False)
        if product is not None:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Erreur, le produit n'existe pas ou est deja vendu.")

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            # TODO: on notifie par mail l'auteur du produit.
            # TODO: Si on a plus d'info a donner on demande ca par mail à l'auteur du report.
        return JsonResponse({
            'message': "Tu as signalé le produit. Il est possible qu'on te contacte pour plus d'informations.",
            'data': serializer.validated_data
        }, status=status.HTTP_201_CREATED)


class ReviewReportView(viewsets.ModelViewSet):
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReviewReport.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        create_review_report(serializer, self.request.user, self.kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            # TODO: on notifie par mail le vendeur.
            # TODO: Si on a plus d'info a donner on demande ca par mail à l'auteur du report.
        return JsonResponse({
            'message': "Tu as signalé l'avis. Il est possible qu'on te contacte pour plus d'informations.",
            'data': serializer.validated_data
        }, status=status.HTTP_201_CREATED)


class ReviewReplyReportView(viewsets.ModelViewSet):
    serializer_class = ReviewReplyReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReviewReplyReport.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        create_reply_report(serializer, self.request.user, self.kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            # TODO: on notifie par mail le vendeur.
            # TODO: Si on a plus d'info a donner on demande ca par mail à l'auteur du report.
        return JsonResponse({
            'message': "Tu as signalé l'avis. Il est possible qu'on te contacte pour plus d'informations.",
            'data': serializer.validated_data
        }, status=status.HTTP_201_CREATED)
