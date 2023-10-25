from django.urls import path

from Domain.phone.views import PhoneView

urlpatterns = [
    path('profile/phone/<int:pk>/update', PhoneView.as_view({'patch': 'update'})),
    path('profile/phone/<int:pk>/delete', PhoneView.as_view({'delete': 'destroy'})),
    path('profile/phone/create', PhoneView.as_view({'post': 'create'})),
    path('profile/phones/all', PhoneView.as_view({'get': 'list'})),

]
