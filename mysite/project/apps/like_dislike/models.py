from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings


"""
                    Article
                      /
Like:ForeingK
                      \
                       Comment
"""
class BaseLike(models.Model):
    data = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
    

class Like(BaseLike):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True)


class Subscribe(BaseLike):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)


