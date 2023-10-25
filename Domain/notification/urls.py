from django.urls import path

from Domain.notification.views import home
from Domain.offer.views import OfferView

urlpatterns = [
    path('index/', home),
]
