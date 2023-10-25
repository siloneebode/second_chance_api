from django.urls import path
from Domain.category.views import CategoryListView, SubCategoryView, EndCategoryView

urlpatterns = [
    path('subcategories/', SubCategoryView.as_view({'get': 'list', })),
    path('<str:category_slug>/<str:sub_category_slug>/', SubCategoryView.as_view({'get': 'get_sub_category'})),
]
