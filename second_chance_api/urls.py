from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/' + settings.API_VERSION + '/', include("Domain.urls")),
    path('', include("Domain.notification.urls")),
]
