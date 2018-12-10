from django.urls import path, register_converter
from . import views, converters
from .models import  Article, Thread
from .forms import CreatePostForm, CreateArticleForm, CreateThreadForm
from django.views.generic import RedirectView
from project.apps.account.views import Subscribe


register_converter(converters.CategoryConverter, 'threads')
app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page'}, name='main_page'),

    path('home/', views.MainPage.as_view(),
         {'template_name': 'blog/Home.html', 'location': 'home'}, name='home'),

##

    path('thread/<threads:thread>/top/', views.ThreadsView.as_view(template_name='blog/thread.html'),
         {'location': 'thread/sort/top'}, name='thread-top'),

    path('thread/<threads:thread>/new/', views.ThreadsView.as_view(template_name='blog/thread.html'),
         {'location': 'thread/sort/all'}, name='thread-new'),

    path('thread/<threads:thread>/hot/', views.ThreadsView.as_view(template_name='blog/thread.html'),
         {'location': 'thread/sort/hot'}, name='thread-hot'),

    path('thread/<threads:key>/subscribe/', Subscribe.as_view(model=Thread), name='subscribe-thread'),


    path('thread/<threads:thread>/', RedirectView.as_view(pattern_name='blog:thread-hot'), name='thread'),

##

    path('threads/new/', views.ThreadsView.as_view(template_name='blog/Toptreads.html'),
          {'location': 'thread-list/all', 'search': 'thread'}, name='threads-new'),

    path('threads/top/', views.ThreadsView.as_view(template_name='blog/Toptreads.html'),
         {'location': 'thread-list/top', 'search': 'thread'}, name='threads-top'),

    path('threads/', RedirectView.as_view(pattern_name='blog:threads-top'), name='threads'),


##
    path('users/', views.MainPage.as_view(),
         {'template_name': 'blog/Users.html',  'location': 'users'}, name='users'),


    path('post/<slug:login>/<int:pk>/', views.DetailArticle.as_view(), name='detail_article'),

    path('create-article/', views.CreateArticle.as_view(form_class=CreateArticleForm,
                                                        status='A', model=Article),
                                                        name='create_article'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm,
                                                     status='P', model=Article, not_success='/'),
                                                    {'not-get': True},
                                                     name='create_post'),

    path('create-thread/', views.CreateArticle.as_view(form_class=CreateThreadForm, model=Thread),
                                                      name='create_thread'),
]
