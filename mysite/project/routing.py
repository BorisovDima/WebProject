from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from project.apps.comments.routing import ws_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(        # cookie - user - session - authoriz
        URLRouter(ws_urlpatterns )
    ),
})