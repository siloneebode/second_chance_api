from django.urls import path

from Domain.account.views import UserDetailsView, UserUpdateView
from Domain.phone.views import PhoneView

urlpatterns = [
    path('account/user/active/<int:pk>', UserDetailsView.as_view({'get': 'retrieve'})),
    path('account/user/edit/<int:pk>', UserUpdateView.as_view({'post': 'update'})),
]


