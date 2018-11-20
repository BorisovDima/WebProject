from django.db import models
from project.apps.blog.models import BaseArticle, Article
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import LikeDislike
from django.conf import settings


class Comment(BaseArticle):
    text = models.TextField(max_length=5024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('delete'))
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET('delete'), default='root')
    rating = GenericRelation(LikeDislike, related_query_name='Comment')



