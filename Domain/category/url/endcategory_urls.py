from django.urls import path
from Domain.category.views import CategoryListView, SubCategoryView, EndCategoryView

urlpatterns = [
    path('<str:category_slug>/<str:sub_category_slug>/<str:end_category_slug>/',
         EndCategoryView.as_view({'get': 'get_end_category'})),
    path('endcategories/', EndCategoryView.as_view({'get': 'list', })),

]
