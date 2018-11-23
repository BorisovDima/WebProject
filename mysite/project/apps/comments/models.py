from django.db import models
from project.apps.blog.models import BaseArticle, Article
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import LikeDislike
from django.conf import settings
from  django.urls import reverse

class MyManager(models.Manager):

    def add_comment(self, **kwargs):
        obj = self.create(**kwargs)
        return obj.id

    def get_comment(self, id):
        return self.get(id=id)


class Comment(BaseArticle):
    text = models.TextField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    rating = GenericRelation(LikeDislike, related_query_name='Comment')

    objects = MyManager()

    class Meta:
        ordering = ['-id']

    #def get_absolute_url(self):
        #return 'comment-' + str(self.id)



