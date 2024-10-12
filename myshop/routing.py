from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from mytest import consumers

websocket_urlpatterns = [
    path('ws/scene-change/', consumers.SceneChangeConsumer.as_asgi()),
    re_path(r'ws/device/(?P<device_id>\w+)/$', consumers.DeviceConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter(websocket_urlpatterns ))
})