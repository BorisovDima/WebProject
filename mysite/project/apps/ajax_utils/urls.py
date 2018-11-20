from django.urls import path
from . import views
from project.apps.blog.models import Article
from project.apps.comments.models import Comment

app_name = 'ajax_utils'

urlpatterns = [
    path('load/articles/', views.Loader.as_view(model=Article,
                                           template_name='blog/articles.html'), name='art_loader'),
    path('load/comments/', views.Loader.as_view(model=Comment,
                                           template_name='comments/comments.html'), name='comm_loader'),

]