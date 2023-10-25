from django.urls import path
from Domain.product.views import ProductView

urlpatterns = [
    path("products/step-1/create/", ProductView.as_view({'post': 'create'})),
    path("products/<int:pk>/step-2/add/", ProductView.as_view({'post': 'product_add'})),
    path("products/<int:pk>/visible/", ProductView.as_view({'post': 'set_visible'})),
    path("products/<int:pk>/republish/", ProductView.as_view({'post': 'republish'})),
    path("products/<int:pk>/remove/", ProductView.as_view({'delete': 'product_delete'})),
    path("products/<int:pk>/edit/", ProductView.as_view({'post': 'partial_update'})),
    path("<str:category_slug>/<str:sub_category_slug>/<str:end_category_slug>/<str:product_slug>/", ProductView.as_view({'get': 'product_detail'}))
]
