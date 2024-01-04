import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chats.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')

# Get the Django ASGI application
django_asgi_application = get_asgi_application()

# WebSocket application
websocket_application = AuthMiddlewareStack(
    URLRouter(chats.routing.websocket_urlpatterns)
)

# Combined application for both HTTP and WebSocket
application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": websocket_application,
    }
)
