from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




"""
                    Article
                      /
LikeDislike:ForeingK
                      \
                       Comment
"""

class LikeDislike(models.Model):

    data = ''
    user = ''
    like_dis = ''

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
