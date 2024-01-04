import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chats.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')

# Get the Django ASGI application
django_asgi_application = get_asgi_application()

# WebSocket application
websocket_application = AuthMiddlewareStack(
    URLRouter(websocket_urlpatterns)
)

# Combined application for both HTTP and WebSocket
application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": websocket_application,
    }
)
