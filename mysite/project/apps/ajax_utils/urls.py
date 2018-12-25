from django.urls import path
from . import views
from project.apps.blog.models import Article, Community
from  django.contrib.auth import get_user_model
from project.apps.event_handler.models import Notification
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
                                             sorted_kwargs={'sorted': 'search',
                                                            'option': 'top',
                                                            'field': 'username__icontains',}),
                                                                name='usr_loader'),

    path('load/main-page/communities/', views.Loader_sorted.as_view(model=Community,
                                                                         template_name='blog/communities.html',
                                                                         sorted_kwargs={'field': 'name__icontains',
                                                                                        'sorted': 'search',
                                                                                        'option': 'top',},
                                                                         paginate=10), name='communities'),



    path('load/main-page/people/search-top/', views.Loader_sorted.as_view(model=get_user_model(),
                                             template_name='blog/users.html',
                                             paginate=10,
                                             sorted_kwargs={'sorted': 'search',
                                                            'option': 'top',
                                                            'field': 'username__icontains',}),
                                                                name='usr_loader-top'),

    path('load/main-page/people/search-new/', views.Loader_sorted.as_view(model=get_user_model(),
                                                                          template_name='blog/users.html',
                                                                          sorted_kwargs={'sorted': 'search',
                                                                                         'option': 'new',
                                                                                        'field': 'username__icontains'},
                                                                          paginate=10),
                                                                          name='usr_loader-new'),




    path('load/main-page/community-search/', views.Loader_sorted.as_view(model=Community,
                                                                         template_name='blog/communities.html',
                                                                         sorted_kwargs={'field': 'name__icontains',
                                                                                        'sorted': 'search'},
                                                                         paginate=10), name='communities-search'),


    ###
    path('load/community/<slug:key>/top/', views.Loader_sorted.as_view(model=Article,
                                                            template_name='blog/articles.html',
                                                            sorted_kwargs={'field': 'community__name',
                                                                            'sorted': 'top'}),
                                                            name='art_loader-top'),

    path('load/community/<slug:key>/all/', views.Loader_sorted.as_view(model=Article,
                                                             template_name='blog/articles.html',
                                                             sorted_kwargs={'field': 'community__name',
                                                                            'sorted': 'all'}),
                                                             name='art_loader-all'),

    path('load/community/<slug:key>/hot/', views.Loader_sorted.as_view(model=Article,
                                                             template_name='blog/articles.html',
                                                             sorted_kwargs={'field': 'community__name',
                                                                            'sorted': 'hot'}),
                                                             name='art_loader-hot'),


###




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

    path('load/profile/<slug:key>/community/', views.Loader_sorted.as_view(model=Community,
                                                                           template_name='blog/communities.html',
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