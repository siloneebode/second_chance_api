from django.http.response import JsonResponse
from rest_framework import viewsets, status
from Domain.phone.models import Phone
from Domain.phone.serializers import PhoneSerializer


class PhoneView(viewsets.ModelViewSet):
    http_method_names = ('post', 'get', 'patch', 'delete')
    serializer_class = PhoneSerializer

    def get_queryset(self):
        return Phone.objects.filter(owner=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.filter(pk=self.kwargs['pk'])

    def perform_create(self, serializer):
        if Phone.objects.filter(owner=self.request.user, is_verified=True, for_paiement=True).exists():
            serializer.save(owner=self.request.user)
        else:
           pass
        # TODO: ici on va envoyer le message OTP a l'utilisateur.

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return JsonResponse({
                "data": serializer.validated_data,
                "message": "numéro de téléphone ajouté avec success "
            }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        phone = Phone.objects.filter(pk=kwargs['pk'])
        serializer = self.serializer_class(phone)

        return JsonResponse({
            "data": serializer.data,
            "message": "Address modifié avec success "
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        phone = Phone.objects.filter(pk=kwargs['pk'])
        phone.delete()

        return JsonResponse({'message': 'numéro de téléphone supprimé avec succès'}, status=status.HTTP_200_OK)
