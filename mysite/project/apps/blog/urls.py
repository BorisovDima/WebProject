from django.urls import path, register_converter
from . import views
from .models import  Article, Community
from .forms import CreatePostForm, CreateArticleForm, CreateCommunityForm
from django.views.generic import RedirectView
from project.apps.account.models import Profile


app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'm', 'start_loc': 'm'},
         name='main_page'),

    path('m/', RedirectView.as_view(pattern_name='blog:main_page')),

    path('m/popular/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'm/popular', 'start_loc': 'm'},
         name='popular'),

    path('m/new/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'm/new', 'start_loc': 'm'},
         name='new'),

    path('m/people/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'm/people', 'start_loc': 'm'},
         name='people'),

    path('m/communities/',views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'm/communities', 'start_loc': 'm'},
         name='communities'),

    path('home/', views.MainPage.as_view(),
         {'template_name': 'blog/Home.html', 'location': 'home'}, name='home'),
#

 #   path('community/<slug:slug>/', views.CommunityView.as_view(), name='community'),


   # path('create-article/', views.CreateArticle.as_view(form_class=CreateArticleForm,
    #                                                    status='A', model=Article),
    #                                                    name='create_article'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm,
                                                     model=Article),
                                                     name='create_post'),

  #  path('create-community/', views.CreateArticle.as_view(form_class=CreateCommunityForm, model=Community),
    #                                                  name='create_community'),
    path('api/post/<int:pk>/view/', views.ViewPost.as_view())

]
