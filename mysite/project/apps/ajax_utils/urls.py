from django.urls import path
from . import views
from project.apps.blog.models import Article
from project.apps.account.models import Profile

app_name = 'ajax_utils'

urlpatterns = [
    path('load/articles/', views.Loader.as_view(model=Article,
                                           template_name='blog/articles.html'), name='art_loader'),

    path('load/users/', views.Loader.as_view(model=Profile,
                                                template_name='blog/list_users.html'), name='usr_loader')
]