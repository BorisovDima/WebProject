from django.urls import path
from . import consumers


chat_urlpatterns = [
    path('dialog/<slug:id_dialog>/', consumers.ChatConsumer),
    path('event-handler/', consumers.EventConsumer),

]
