from django.urls import path
from Domain.follower.views import FollowView

urlpatterns = [
    path('profile/<str:slug>-<int:pk>/follow', FollowView.as_view({'post': 'follow'})),
    path('profile/<int:pk>/unfollow', FollowView.as_view({'post': 'partial_update'})),
    # compte tous les followers et les following
    #path('profile/followers', FollowView.as_view()),
]
