from django.urls import path
from django.conf.urls import url
from . import consumers

ws_urlpatterns  = [
    path('<categories:category>/<slug:slug>/', consumers.CommentConsumer),

]

