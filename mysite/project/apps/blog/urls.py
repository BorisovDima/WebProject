from django.urls import path, register_converter
from . import views
from .models import  Article, Community
from .forms import CreatePostForm, CreateArticleForm, CreateCommunityForm
from django.views.generic import RedirectView
from project.apps.account.models import Profile



app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page', 'start_loc': 'main-page'},
         name='main_page'),

    path('popular/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page/popular', 'start_loc': 'main-page'},
         name='popular'),

    path('new/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page/new', 'start_loc': 'main-page'},
         name='new'),

    path('people/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page/people', 'start_loc': 'main-page'},
         name='people'),

    path('communities/',views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'main-page/communities', 'start_loc': 'main-page'},
         name='communities'),

    path('home/', views.MainPage.as_view(),
         {'template_name': 'blog/Home.html', 'location': 'home'}, name='home'),
#

    path('community/<slug:slug>/', views.CommunityView.as_view(), name='community'),


    path('post/<slug:login>/<int:pk>/', views.DetailArticle.as_view(), name='detail_article'),





    path('create-article/', views.CreateArticle.as_view(form_class=CreateArticleForm,
                                                        status='A', model=Article),
                                                        name='create_article'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm,
                                                     status='P', model=Article, not_success='/'),
                                                    {'not-get': True},
                                                     name='create_post'),

    path('create-community/', views.CreateArticle.as_view(form_class=CreateCommunityForm, model=Community),
                                                      name='create_community'),


]
