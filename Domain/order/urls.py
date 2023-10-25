from django.urls import path

from Domain.order.views import OrderView
from Domain.password.views import PasswordResetView, ChangeResetPasswordView
from Domain.phone.views import PhoneView

urlpatterns = [
    path('checkout/<int:product>/create', OrderView.as_view({'post': 'create'})),
    path('order/<int:pk>/refuse', OrderView.as_view({'post': 'refuse_order'})),
    path('order/<int:pk>/accept', OrderView.as_view({'post': 'accept_order'})),
]

