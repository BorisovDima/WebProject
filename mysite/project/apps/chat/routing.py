from django.urls import path
from . import consumers


chat_urlpatterns = [
    path('ws/dialog/<slug:id_dialog>/', consumers.ChatConsumer),

]
