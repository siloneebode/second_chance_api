from django.urls import path, include, re_path

urlpatterns = [
    path('', include("Domain.category.urls")),
    path('', include("Domain.auth.urls")),
    path('', include("Domain.account.urls")),
    path('', include("Domain.phone.urls")),
    path('', include("Domain.reduction.urls")),
    path('', include("Domain.follower.urls")),
    path('', include("Domain.product.urls")),
    path('', include("Domain.brand.urls")),
    path('', include("Domain.offer.urls")),
    path('', include("Domain.order.urls")),
    path('', include("Domain.report.urls")),
    path('', include("Domain.additionalInfo.urls")),
    path('security/', include("Domain.password.urls")),
]
