from django.urls import path

from Domain.additionalInfo.views import AddressView
from django.urls import path

urlpatterns = [
    path('profile/address/add', AddressView.as_view({'post': 'create'})),
    path('profile/address/<int:pk>/update', AddressView.as_view({'post': 'update'})),
]
