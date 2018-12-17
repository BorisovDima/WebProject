from django.urls import path
from django.conf.urls import url
from . import consumers

comment_urlpatterns  = [
    path('ws/post/<slug:thread>/<int:id>/add-comment/', consumers.CommentConsumer),

]

