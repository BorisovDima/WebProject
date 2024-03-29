from django.urls import path
from . import views
from project.apps.comments.models import Comment
from project.apps.blog.models import Article

app_name = 'delete_app'
urlpatterns = [
    path('comment/delete/<int:pk>/', views.DeleteObj.as_view(model=Comment, template_name='delete_app/tag/delete_notify.html'),
         {'event': 'comment', 'action': 'delete'}, name='delete-comment'),

    path('post/delete/<int:pk>/', views.DeleteObj.as_view(model=Article, template_name='delete_app/tag/delete_notify.html'),
         {'event': 'post', 'action': 'delete'}, name='delete-post'),

    path('comment/return/<int:pk>/', views.DeleteObj.as_view(model=Comment, template_name='comments/comment.html'),
         {'event': 'comment', 'action': 'return'}, name='return-comment'),

    path('post/return/<int:pk>/', views.DeleteObj.as_view(model=Article, template_name='blog/articles.html'),
         {'event': 'post', 'action': 'return'}, name='return-post'),

]
