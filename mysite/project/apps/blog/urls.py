from django.urls import path, register_converter
from . import views, converters

register_converter(converters.CategoryConverter, 'categories')
app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'articles'} ,name='main_page'),

    path('<categories:category>/', views.MainPage.as_view(),
         {'template_name': 'blog/MainPage.html', 'location': 'articles'}, name='category', ),

    path('users/', views.MainPage.as_view(),
         {'template_name': 'blog/Users.html',  'location': 'users'}, name='users'),

    path('<categories:category>/<slug:slug>/', views.DetailArticle.as_view(), name='detail_article'),
    path('create-article/', views.CreateArticle.as_view(), name='create_article'),


]
