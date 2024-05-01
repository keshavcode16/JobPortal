import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import core_apps.web_store.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homedecor.settings')


django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(
#                 [re_path('notifications/',consumers.SavePostConsumer.as_asgi())]
#             ))
#         ),
#     }
# )
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                core_apps.web_store.routing.websocket_urlpatterns
            )
        ),
    }
)