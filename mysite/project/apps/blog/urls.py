from django.urls import path, register_converter
from . import views, converters

register_converter(converters.CategoryConverter, 'categoryes')
app_name = 'blog'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('<categoryes:category>/', views.MainPage.as_view(), name='category')
]
