from django.urls import path
from . import views
from project.apps.blog.models import Article
from django.contrib.auth import get_user_model

app_name ='search'

urlpatterns = [
    path('search/posts/', views.Search.as_view(model=Article), {'location': 'posts-search'},
         name='search-posts'),

]
