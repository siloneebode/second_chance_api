from django.urls import path

from Domain.conversation.Utils.consumer import ConversationConsumer
from Domain.notification.consumer import NotificationConsumer

ws_urlpatterns = [
    path("notifications/", ConversationConsumer.as_asgi()),
    path('ac/', NotificationConsumer.as_asgi()),

]
