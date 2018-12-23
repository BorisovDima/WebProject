from django.urls import path
from . import views
from project.apps.blog.models import Article, Thread
from  django.contrib.auth import get_user_model
from project.apps.account.models import Notification
from django.views.generic import RedirectView

app_name = 'ajax_utils'

urlpatterns = [
    path('load/main-page/', views.Loader_sorted.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'sorted': 'top'}),
                                                        name='top_loader'),

    path('load/main-page/popular/', views.Loader_sorted.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'sorted': 'hot',
                                                                       'count': 2}),
                                                        name='popular_loader'),

    path('load/main-page/new/', views.Loader_sorted.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'sorted': 'all'}),
                                                        name='new_loader'),

    path('load/main-page/people/', views.Loader_sorted.as_view(model=get_user_model(),
                                             template_name='blog/users.html',
                                             paginate=10,
                                             sorted_kwargs={'sorted': 'followers'}),
                                             name='usr_loader'),

    path('load/main-page/people-top/', RedirectView.as_view(pattern_name='ajax_utils:usr_loader')),

    path('load/main-page/people-new/', views.Loader_sorted.as_view(model=get_user_model(),
                                                                          template_name='blog/users.html',
                                                                          sorted_kwargs={'sorted': 'all'},
                                                                                            paginate=10),
                                                                            name='usr_loader-new'),


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


    path('load/profile/<slug:key>/followers/', views.Loader_sorted.as_view(model=get_user_model(),
                                           template_name='blog/users.html',
                                           sorted_kwargs={'field': 'subscribe__user_followers__username',
                                                          'sorted': 'all'}),
                                                                name='followers-load'),

    path('load/profile/<slug:key>/following/', views.Loader_sorted.as_view(model=get_user_model(),
                                                                 template_name='blog/users.html',
                                                                 sorted_kwargs={'field': 'my_followers__user__username',
                                                                                'sorted': 'all'}),
                                                                name='following-load'),

    path('load/profile/<slug:key>/community/', views.Loader_sorted.as_view(model=Thread,
                                                                           template_name='blog/threads.html',
                                                                           sorted_kwargs={
                                                                               'field': 'my_followers__user__username',
                                                                               'sorted': 'all',
                                                                               'active': True}),
                                                                 name='commynity-load'),


    path('load/profile/<slug:key>/', views.Loader_sorted.as_view(model=Article,
                                                                 template_name='blog/articles.html',
                                                                 sorted_kwargs={'field': 'author__username',
                                                                                'sorted': 'all'}),
                                                                    name='art_loader'),


    path('load/main-page/community-search/', views.Loader_sorted.as_view(model=Thread,
                                                  template_name='blog/threads.html',
                                                  sorted_kwargs={'field': 'name__icontains',
                                                                 'sorted': 'search'},
                                                  paginate=10), name='thread-search'),

    path('load/main-page/people-search/', views.Loader_sorted.as_view(model=get_user_model(),
                                                            template_name='blog/users.html',
                                                            sorted_kwargs={'field': 'username__icontains',
                                                                           'sorted': 'search'},
                                                            paginate=10), name='people-search'),



    path('load/home/', views.Loader_home.as_view(model=Article,
                                                template_name='blog/articles.html',
                                                paginate=15), name='home-feed'),



    path('load/dialogs/', views.Loader_dialogs.as_view(model=get_user_model(),
                                                       template_name='chat/list_dialog.html',
                                                       paginate=15), name='dialogs-loader'),

    path('load/notify/', views.Loader_notify.as_view(model=Notification,
                                                     template_name='event_handler/notifications.html',
                                                     paginate=5,), name='notify-loader'),

]