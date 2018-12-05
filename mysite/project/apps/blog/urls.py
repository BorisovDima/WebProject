from django.urls import path, register_converter
from . import views, converters
from .models import  Article, Thread
from .forms import CreatePostForm, CreateArticleForm


register_converter(converters.CategoryConverter, 'threads')
app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page'} ,name='main_page'),

    path('<threads:thread>/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'thread'}, name='thread'),

    path('threads/all/', views.ThreadsView.as_view(), { 'location': 'thread-list', 'status': 'all'},
         name='threads_all'),

    path('threads/top/', views.ThreadsView.as_view(queryset=Thread.objects.get_top()),
                                                    {'location': 'thread-list'},
                                                    name='threads'),

    path('users/', views.MainPage.as_view(),
         {'template_name': 'blog/Users.html',  'location': 'users'}, name='users'),

    path('<slug:login>/<int:pk>/', views.DetailArticle.as_view(), name='detail_article'),

    path('create-article/', views.CreateArticle.as_view(form_class=CreateArticleForm, status='A'),
         name='create_article'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm, status='P'),
         name='create_post'),


]
