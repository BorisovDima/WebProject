from django.urls import path
from . import views, models
from project.apps.blog.models import Article
from project.apps.comments.models import Comment
from django.contrib.auth import get_user_model


app_name = 'like'
urlpatterns = [
    path('like/post/<int:id>/', views.LikeSubscribe.as_view(model=Article, foreign_model=models.Like,
                                                            type='A',
                                                            event='like'),
                                                            name='post-like'),

    path('like/comment/<int:id>/', views.LikeSubscribe.as_view(model=Comment, foreign_model=models.Like,
                                                               type='C',
                                                               event='like'),
                                                               name='comment-like'),

    path('subscribe/user/<int:id>/', views.LikeSubscribe.as_view(model=get_user_model(), foreign_model=models.Subscribe,
                                                                 type='U',
                                                                 event='subs'),
                                                                 name='subscribe-user'),
]
