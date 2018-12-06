from django.urls import path, register_converter
from . import views, converters
from .models import  Article, Thread
from .forms import CreatePostForm, CreateArticleForm, CreateThreadForm


register_converter(converters.CategoryConverter, 'threads')
app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page'} ,name='main_page'),

    path('thread/<threads:thread>/', views.ThreadsView.as_view(template_name='blog/thread.html'),
         {'location': 'thread'}, name='thread'),

    path('threads/all/', views.ThreadsView.as_view(template_name='blog/Toptreads.html'),
                                            { 'location': 'thread-list', 'status': 'all'},
                                                        name='threads_all'),

    path('threads/top/', views.ThreadsView.as_view(context_object=Thread.objects.get_top,
                                                   template_name='blog/Toptreads.html'),
                                                    {'location': 'thread-list'},
                                                    name='threads'),

    path('users/', views.MainPage.as_view(),
         {'template_name': 'blog/Users.html',  'location': 'users'}, name='users'),

    path('post/<slug:login>/<int:pk>/', views.DetailArticle.as_view(), name='detail_article'),

    path('create-article/', views.CreateArticle.as_view(form_class=CreateArticleForm,
                                                        status='A', model=Article),
                                                        name='create_article'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm,
                                                     status='P', model=Article, not_success='/'),
                                                     name='create_post'),

    path('create-thread/', views.CreateArticle.as_view(form_class=CreateThreadForm, model=Thread),
                                                      name='create_thread'),
]
