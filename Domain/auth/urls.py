from django.urls import path

from Domain.auth import views
from Domain.auth.views import RegisterView, LoginView, RefreshTokenView
from django.urls import path

urlpatterns = [
    path('register', RegisterView.as_view({'post': 'create'})),
    path('login', LoginView.as_view({'post': 'create'})),
    path('refresh', RefreshTokenView.as_view({'post': 'create'})),
    path('profile/email-verification/send/<int:pk>', RegisterView.as_view({'post': 'send_verification_email'})),
    path('profile/email-verification/<str:token>/confirm', RegisterView.as_view({'post': 'confirm_account'}),
         name='profile_account_confirm'),
    path('profile/verification/registration-fields', RegisterView.as_view({'post': 'registration_validation'}))
]
