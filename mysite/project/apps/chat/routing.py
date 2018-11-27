from django.urls import path
from . import consumers


chat_urlpatterns  = [
    path('dialog/<int:id_dialog>/', consumers.ChatConsumer),
]
