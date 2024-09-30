from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/localhost:3000/$', consumers.MtechConsumer.as_asgi()),
]