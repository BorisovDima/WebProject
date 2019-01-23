from django.urls import path
from . import views
from .models import  Article
from .forms import CreatePostForm, UpdatePostForm
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [

    path('', RedirectView.as_view(pattern_name='blog:main_page')),

    path('m/', views.MainPage.as_view(template_name = 'blog/MainPage.html'),
         {'location': 'top', 'title': 'Signup: Main page'},
         name='main_page'),

    path('home/', login_required(views.MainPage.as_view(template_name = 'blog/Home.html')),
         {'template_name': 'blog/Home.html', 'location': 'home', 'title': 'Home'},
         name='home'),

    path('create-post/', views.CreateArticle.as_view(form_class=CreatePostForm, model=Article, success_url = '/'),
         name='create_post'),

    path('update-post/<int:pk>/', views.UpdateArticle.as_view(form_class=UpdatePostForm,
         template_name='blog/update_post.html', model=Article, success_url = '/'),
         name='update_post'),

    path('api/post/detail-post/<int:pk>/', views.DetailArticle.as_view(model=Article,
                                                                       template_name = 'blog/articles.html')),

    path('api/home/recommends/', views.Recommend.as_view()),

    path('m/<path:location>/', views.MainPage.as_view(template_name = 'blog/MainPage.html'),
         {'title': 'Signup: Main page'}),
]

