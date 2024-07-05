from django.urls import re_path
from .consumers import SavePostConsumer

websocket_urlpatterns = [
    re_path(
        'notifications/(?P<threadId>\w+)/',
        SavePostConsumer.as_asgi()
    ),
]