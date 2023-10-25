from django.urls import path

from Domain.password.views import PasswordResetView, ChangeResetPasswordView
from Domain.phone.views import PhoneView

urlpatterns = [
    path('password/reset', PasswordResetView.as_view({'post': 'create'})),
    path('password/<str:token>/confirm', PasswordResetView.as_view({'post': 'confirm_reset'})),
    path('password/<str:slug>-<int:pk>/change', ChangeResetPasswordView.as_view({'patch': 'partial_update'})),

]
