from django.urls import path
from . import views
from project.apps.blog.models import Article, Thread
from project.apps.account.models import Profile
from django.conf import settings
from  django.contrib.auth import get_user_model
app_name = 'ajax_utils'

urlpatterns = [
    path('load/main-page/', views.Loader_sorted.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'sorted': 'top'}),
                                                        name='art_loader'),

    path('load/users/', views.Loader_sorted.as_view(model=Profile,
                                             template_name='blog/list_users.html',
                                             paginate=15,
                                             sorted_kwargs={'sorted': 'all'}),
                                             name='usr_loader'),



    path('load/thread/<slug:key>/top/', views.Loader_sorted.as_view(model=Article,
                                                            template_name='blog/articles.html',
                                                            sorted_kwargs={'field': 'thread__name',
                                                                            'sorted': 'top'}),
                                                            name='art_loader-top'),

    path('load/thread/<slug:key>/all/', views.Loader_sorted.as_view(model=Article,
                                                             template_name='blog/articles.html',
                                                             sorted_kwargs={'field': 'thread__name',
                                                                            'sorted': 'all'}),
                                                             name='art_loader-all'),

    path('load/thread/<slug:key>/hot/', views.Loader_sorted.as_view(model=Article,
                                                             template_name='blog/articles.html',
                                                             sorted_kwargs={'field': 'thread__name',
                                                                            'sorted': 'hot'}),
                                                             name='art_loader-hot'),


    path('load/user-articles/<slug:key>/', views.Loader_sorted.as_view(model=Article,
                                           template_name='blog/articles.html',
                                           sorted_kwargs={'field': 'author__username',
                                                          'sorted': 'all'}),
                                           name='art_loader'),



    path('load/thread-list/all/', views.Loader_sorted.as_view(model=Thread,
                                                  template_name='blog/threads.html',
                                                  paginate=20,
                                                  sorted_kwargs={'sorted': 'all'}),
                                                  name='thread-all'),

    path('load/thread-list/top/', views.Loader_sorted.as_view(model=Thread,
                                                       template_name='blog/threads.html',
                                                       paginate=20,
                                                       sorted_kwargs={'sorted': 'top'}),
                                                       name='thread-top'),



    path('load/thread-search/', views.Loader_search.as_view(model=Thread,
                                                  template_name='blog/threads.html',
                                                  sorted_kwargs={'field': 'name__icontains'},
                                                  paginate=20), name='thread-search'),

    path('load/home/', views.Loader_home.as_view(model=Article,
                                                template_name='blog/articles.html',
                                                paginate=15), name='home-feed'),


    path('load/dialogs/<int:id>/', views.Loader_dialogs.as_view(model=get_user_model(),
                                                       template_name='chat/list_dialog.html',
                                                       paginate=15),
                                                       name='dialogs-loader'),

]