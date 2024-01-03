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
from chats.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insight.settings')

def application(scope, receive, send):
    # Any Django-related imports should be inside this function
    return ProtocolTypeRouter(
        {
            'http': get_asgi_application(),
            'websocket': URLRouter(websocket_urlpatterns),
        }
    )(scope, receive, send)
