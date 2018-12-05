from django.urls import path
from .import consumers

event_urlpatterns = [
    path('ws/event-handler/', consumers.EventConsumer),
]
