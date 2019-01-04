from django.urls import path
from . import views
from project.apps.blog.models import Article, Community
from django.contrib.auth import get_user_model
from project.apps.event_handler.models import Notification
from project.apps.comments.models import Comment


app_name = 'ajax_utils'

urlpatterns = [
    path('load/m/', views.Top.as_view(model=Article,
                                                        template_name='blog/articles.html'),
                                                        name='top_loader'),

    path('load/m/popular/', views.Hot.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'count': 2}),
                                                        name='popular_loader'),

    path('load/m/new/', views.All.as_view(model=Article,
                                                        template_name='blog/articles.html'),
                                                        name='new_loader'),

    path('load/m/people/', views.Search.as_view(model=get_user_model(),
                                             template_name='blog/users.html',
                                             paginate=10,
                                             sorted_kwargs={'option': 'top',
                                                            'field': 'username__icontains',
                                                            'top_field': 'my_followers'}),
                                                                name='usr_loader'),

    path('load/m/communities/', views.Search.as_view(model=Community,
                                                                         template_name='blog/communities.html',
                                                                         sorted_kwargs={'field': 'name__icontains',
                                                                                        'option': 'top',
                                                                                        'top_field': 'my_followers'},
                                                                         paginate=10), name='communities'),



    path('load/m/people/search-top/', views.Search.as_view(model=get_user_model(),
                                             template_name='blog/users.html',
                                             paginate=10,
                                             sorted_kwargs={'option': 'top',
                                                            'field': 'username__icontains',
                                                            'top_field': 'my_followers'}),
                                                                name='usr_loader-top'),

    path('load/m/people/search-new/', views.Search.as_view(model=get_user_model(),
                                                                          template_name='blog/users.html',
                                                                          sorted_kwargs={'option': 'new',
                                                                                        'field': 'username__icontains'},
                                                                          paginate=10),
                                                                          name='usr_loader-new'),


    path('load/m/community-search/', views.Search.as_view(model=Community,
                                                                         template_name='blog/communities.html',
                                                                         sorted_kwargs={'field': 'name__icontains',
                                                                                        },
                                                                         paginate=10), name='communities-search'),



   # path('load/community/<slug:key>/top/', views.Loader_sorted.as_view(model=Article,
                                                           # template_name='blog/articles.html',
                                                           # sorted_kwargs={'field': 'community__name',
                                                          #                  'sorted': 'top'}),
                                                           # name='art_loader-top'),

   # path('load/community/<slug:key>/all/', views.Loader_sorted.as_view(model=Article,
                                                           #  template_name='blog/articles.html',
                                                          #   sorted_kwargs={'field': 'community__name',
                                                          #                  'sorted': 'all'}),
                                                          #   name='art_loader-all'),

   # path('load/community/<slug:key>/hot/', views.Loader_sorted.as_view(model=Article,
                                                         #    template_name='blog/articles.html',
                                                         #    sorted_kwargs={'field': 'community__name',
                                                         #                   'sorted': 'hot'}),
                                                         #    name='art_loader-hot'),






    path('load/profile/<slug:key>/followers/', views.All.as_view(model=get_user_model(),
                                           template_name='blog/users.html',
                                           sorted_kwargs={'field': 'subscribe__user_followers__username',
                                                          }),
                                                                name='followers-load'),

    path('load/profile/<slug:key>/following/', views.All.as_view(model=get_user_model(),
                                                                 template_name='blog/users.html',
                                                                 sorted_kwargs={'field': 'my_followers__user__username',
                                                                                }),
                                                                name='following-load'),

    path('load/profile/<slug:key>/community/', views.All.as_view(model=Community,
                                                                           template_name='blog/communities.html',
                                                                           sorted_kwargs={
                                                                               'field': 'my_followers__user__username',
                                                                               'active': True}),
                                                                 name='commynity-load'),


    path('load/profile/<slug:key>/', views.All.as_view(model=Article,
                                                                 template_name='blog/articles.html',
                                                                 sorted_kwargs={'field': 'author__username',
                                                                                }),
                                                                    name='art_loader'),



    path('load/home/', views.Home.as_view(model=Article,
                                                template_name='blog/articles.html',
                                                paginate=15),
                                                name='home-feed'),



    path('load/dialogs/', views.Loader_dialogs.as_view(model=get_user_model(),
                                                       template_name='chat/list_dialog.html',
                                                       paginate=15), name='dialogs-loader'),

    path('load/notify/', views.Loader_notify.as_view(model=Notification,
                                                     template_name='event_handler/notifications.html',
                                                     paginate=5,), name='notify-loader'),

    path('post/comments/<int:key>/', views.Loader_comments.as_view(model=Comment,
                                                                template_name='comments/comments.html')),

    path('load/posts-search/', views.Search.as_view(model=Article,
                                                        template_name='blog/articles.html',
                                                        sorted_kwargs={'option': 'top',
                                                                    'field': 'text__icontains',
                                                                    'top_field': 'views'},
                                                           )),

    path('load/people-search/', views.Search.as_view(model=get_user_model(),
                                                        template_name='blog/users.html',
                                                        sorted_kwargs={'option': 'top',
                                                                    'field': 'username__icontains',
                                                                    'top_field': 'my_followers'},
                                                            ))



]