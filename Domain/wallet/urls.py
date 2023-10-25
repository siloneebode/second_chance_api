from django.urls import path
from Domain.wallet.views import WalletView

urlpatterns = [
    path('profile/wallet', WalletView.as_view({'get': 'list'})),
    path('profile/wallet/<str:token>/activate', WalletView.as_view({'patch': 'update'})),

]