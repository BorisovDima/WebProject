from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from project.apps.comments.routing import comment_urlpatterns
from project.apps.event_handler.routing import event_urlpatterns
from project.apps.chat.routing import chat_urlpatterns

pattern = comment_urlpatterns + event_urlpatterns + chat_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(        # cookie - user - session - authoriz
        URLRouter(pattern)
    ),
})

