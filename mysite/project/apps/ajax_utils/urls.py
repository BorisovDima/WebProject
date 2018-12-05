from django.urls import path
from . import views
from project.apps.blog.models import Article, Thread
from project.apps.account.models import Profile

app_name = 'ajax_utils'

urlpatterns = [
    path('load/main-page/', views.Loader.as_view(model=Article,
                                                 template_name='blog/articles.html'),
                                                 name='art_loader'), #sorted_kwargs={'field': 'thread'}

    path('load/users/', views.Loader.as_view(model=Profile,
                                             template_name='blog/list_users.html',
                                             paginate=15), name='usr_loader'),

    path('load/thread/<slug:key>/', views.Loader.as_view(model=Article,
                                           template_name='blog/articles.html',
                                           sorted_kwargs={'field': 'thread'}),
                                           name='art_loader'),

    path('load/user-articles/<slug:key>/', views.Loader.as_view(model=Article,
                                           template_name='blog/articles.html',
                                           sorted_kwargs={'field': 'author__username'}),
                                           name='art_loader'),

    path('load/thread-list/', views.Loader.as_view(model=Thread,
                                                  template_name='blog/threads.html',
                                                  paginate=20),
                                                  name='thread_loader'),

    path('load/thread-list-search/', views.Loader.as_view(model=Thread,
                                                  template_name='blog/threads.html',
                                                  sorted_kwargs={'field': 'name__icontains'},
                                                  paginate=20), name='thread_loader')


]