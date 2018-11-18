from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.MainPage, name='main_page')
]
