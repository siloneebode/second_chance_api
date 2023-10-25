from django.urls import path, include

from Domain.brand.views import BrandView

urlpatterns = [
    path("brands/", BrandView.get_queryset),
    path("brands/<str:brand_slug>", BrandView.get_product_by_brand),
]