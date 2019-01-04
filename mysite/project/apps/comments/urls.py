from django.urls import path
from . import views
from .models import Comment
from project.apps.blog.models import Article

app_name = 'comments'
urlpatterns = [

    path('load-comment-child/<int:pk>/', views.GetChild.as_view(model=Comment,
                                            template_name='comments/child_comments_list.html'))
]
