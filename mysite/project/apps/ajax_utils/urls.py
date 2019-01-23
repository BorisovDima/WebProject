from django.urls import path
from . import views
from project.apps.blog.models import Article
from django.contrib.auth import get_user_model
from project.apps.event_handler.models import Notification
from project.apps.comments.models import Comment
from project.apps.chat.models import Dialog, Message

app_name = 'ajax_utils'

urlpatterns = [

    path('load/post/<path:location>/',
         views.AjaxLoaderView.as_view(model=Article, template_name='blog/articles.html'), name='ajax-load-post'),
    path('load/user/<path:location>/',
         views.AjaxLoaderView.as_view(model=get_user_model(), template_name='blog/users.html')),
    path('load/comment/<path:location>/',
         views.AjaxLoaderView.as_view(model=Comment, template_name='comments/comments.html')),
    path('load/notify/<path:location>/',
         views.AjaxLoaderView.as_view(model=Notification, template_name='event_handler/notifications.html')),
    path('load/dialog/<path:location>/',
         views.AjaxLoaderView.as_view(model=Dialog, template_name='chat/list_dialog.html')),
    path('load/message/<path:location>/',
         views.AjaxLoaderView.as_view(model=Message, template_name='chat/messages.html')),
]

