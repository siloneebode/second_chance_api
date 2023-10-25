from django.urls import path, include
from Domain.category.views import CategoryListView, SubCategoryView, EndCategoryView

urlpatterns = [
    path('', include("Domain.category.url.subcategory_urls")),
    path('', include("Domain.category.url.endcategory_urls")),
    path('categories/', CategoryListView.as_view({'get': 'list', })),
    path('<str:category_slug>/', CategoryListView.as_view({'get': 'get_category'})),
]
