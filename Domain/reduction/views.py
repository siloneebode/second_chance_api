from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from Domain.reduction.models import Reduction
from Domain.reduction.serializers import ReductionSerializer


class ReductionView(viewsets.ModelViewSet):
    serializer_class = ReductionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reduction.objects.filter(owner=self.request.user)

    def get_object(self):
        return self.get_queryset().filter(pk=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return JsonResponse({
                'data': serializer.validated_data,
                'message': 'réduction ajoutée avec succès'
            }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        reduction = self.serializer_class(self.get_object())
        reduction.save()

        return JsonResponse({'data': reduction.validated_data, 'message': 'réduction mis à jour avec succès'},
                            status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
        except Reduction.DoesNotExist:
            return JsonResponse('message', "Erreur Inconnue, réessayez plus tard, "
                                           "si l'erreur persiste contactez notre support")

        return JsonResponse('message', "réduction supprimée avec succès")
