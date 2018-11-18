from django.db import models
from project.apps.blog.models import BaseArticle
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike import LikeDislike

class Comment(BaseArticle):
    #
    #
    #
    rating = GenericRelation(LikeDislike, related_query_name='comment')


