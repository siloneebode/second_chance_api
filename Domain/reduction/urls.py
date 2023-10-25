from django.urls import path

from Domain.reduction.views import ReductionView

urlpatterns = [
    path('profile/reduction/<int:pk>/update', ReductionView.as_view({'patch': 'update'})),
    path('profile/reduction/<int:pk>/delete', ReductionView.as_view({'delete': 'destroy'})),
    path('profile/reduction/create', ReductionView.as_view({'post': 'create'})),
    path('profile/reductions/', ReductionView.as_view({'get': 'list'})),

]