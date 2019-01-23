from django.urls import path
from . import consumers

comment_urlpatterns  = [
    path('ws/post/<int:id>/add-comment/', consumers.CommentConsumer),

]

