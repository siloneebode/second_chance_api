from django.http import JsonResponse
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from Domain.Utils.Mixins.mixins import MultipleFieldLookupMixin
from Domain.product.models import Product
from Domain.product.serializers import ProductSerializer, ProductDetailSerializer
from Domain.product.services import update, create_product


class ProductView(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_fields = ['category_slug', 'sub_category_slug', 'end_category_slug', 'product_slug']

    def get_queryset(self):
        return Product.objects.filter(active=True)

    @action(['GET'], detail=True)
    def get_product(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(product_slug=kwargs['product_slug'])
            serializer = ProductDetailSerializer(product)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'message': 'Erreur, article introuvable'})

        return JsonResponse(serializer.data,
                            status=status.HTTP_200_OK)

    # Dans le perform create je passe le owner et je passe le is_draft à false
    def perform_create(self, serializer):
        create_product(serializer, self.request.user)
        serializer.save(owner=self.request.user, is_draft=True)

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        return JsonResponse({
            'message': 'produit ajouté avec succes',
            'data': serializer.validated_data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def set_visible(self, request, *args, **kwargs):
        # on recherche si le produit existe en base de donnée
        try:
            product = Product.objects.get(pk=kwargs['pk'])
        except Product.DoesNotExist:
            raise serializers.ValidationError({"message": 'Erreur, article introuvable'})

        # s'il existe on regarde son état de visibilité et on change
        if product.is_visible:
            product.is_visible = False
            product.save()
            return JsonResponse({"message": "Produit masqué, plus personne ne pourra plus le voir à part vous"},
                                status=status.HTTP_200_OK)
        else:
            product.is_visible = True
            product.save()

        return JsonResponse({"message": "Produit de nouveau visible, tout le monde peut désormais le voir. "},
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def republish(self, request, *args, **kwargs):

        # on recherche si le produit existe en base de donnée
        try:
            product = Product.objects.get(pk=kwargs['pk'])
            product2 = product
            product2.id = None
            product2.is_sold = False
            product2.save()
        except Product.DoesNotExist:
            raise serializers.ValidationError({"message": 'Erreur, article introuvable'})

        return JsonResponse({'message': 'produit republié avec succès'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def product_delete(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs['pk'])
            product.delete()
            # TODO: On ne doit jamais supprimé un article, on va trouver le moyen de cacher ca à l'utilisateur

        except Product.DoesNotExist:
            raise serializers.ValidationError({"message": 'Erreur, article introuvable'})

        return JsonResponse({"message": "Produit supprimé avec succès"}, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer, images = ProductSerializer(product)

        # TODO: Ici on passe encore à un service pour la modification.
        product = update(serializer, images)

        return JsonResponse({"message": "article modifié avec succès"},
                            status=status.HTTP_401_UNAUTHORIZED)
