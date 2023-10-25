from django.urls import path

from Domain.reduction.views import ReductionView
from Domain.report.views import UserReportView, ProductReportView, ReviewReportView, ReviewReplyReportView

urlpatterns = [
    path('profile/report/user/<int:seller>/create', UserReportView.as_view({'post': 'create'})),
    path('profile/report/product/<int:product>/create', ProductReportView.as_view({'post': 'create'})),
    path('profile/report/review/<int:review>/create', ReviewReportView.as_view({'post': 'create'})),
    path('profile/report/reply/<int:reply>/create', ReviewReplyReportView.as_view({'post': 'create'})),
]
