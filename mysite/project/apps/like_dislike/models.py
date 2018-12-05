from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings


"""
                    Article
                      /
LikeDislike:ForeingK
                      \
                       Comment
"""

class LikeDislike(models.Model):

    VOTES = (
        (1, 'Like'),
        (-1, 'Dislike')
    )


    data = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET('delete'))
    vote = models.IntegerField(choices=VOTES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
