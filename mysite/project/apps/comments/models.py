from django.db import models
from project.apps.blog.models import BaseArticle, Article
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import Like
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class MyManager(models.Manager):

    def add_comment(self, **kwargs):
        obj = self.create(**kwargs)
        return obj.id


    def get_comment(self, id):
        return self.get(id=id)





class Comment(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=424)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    like = GenericRelation(Like, related_query_name='Comment')
    is_active = models.BooleanField(default=True)
    initial_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='initial_comment_set'
                                         ,blank=True, null=True)

    objects = MyManager()

    def _delete(self, *args, **kwargs):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def _return(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    class Meta:
        ordering = ['-id']

    #def get_absolute_url(self):
        #return 'comment-' + str(self.id)


