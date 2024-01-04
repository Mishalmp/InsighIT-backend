# """
# ASGI config for insight project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter,URLRouter
# from chats.routing import websocket_urlpatterns


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')

# application = ProtocolTypeRouter(
#     {
#         'http':get_asgi_application(),
#         'websocket':(
#             (URLRouter(websocket_urlpatterns))
#         )
#     }
# )

"""
ASGI config for insight project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chats.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')

# Get the Django ASGI application
django_asgi_application = get_asgi_application()

# WebSocket application
websocket_application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)

# Combined application for both HTTP and WebSocket
application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": websocket_application,
    }
)
