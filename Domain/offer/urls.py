from django.urls import path
from Domain.offer.views import OfferView

urlpatterns = [
    path('profile/offer/<int:product>/<int:seller>/create', OfferView.as_view({'post': 'create'})),
    path('profile/offer/<int:pk>/accept', OfferView.as_view({'post': 'accept'})),
    path('profile/offer/<int:pk>/deny', OfferView.as_view({'post': 'deny'})),
]
