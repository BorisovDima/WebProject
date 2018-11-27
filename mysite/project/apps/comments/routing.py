from django.urls import path
from django.conf.urls import url
from . import consumers

comment_urlpatterns  = [
    path('<categories:category>/<slug:slug>/add-comment/', consumers.CommentConsumer),

]

