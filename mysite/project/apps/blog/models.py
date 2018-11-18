from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike import LikeDislike
from django.conf import settings
class BaseArticle(models.Model):

    create_data = models.DateTimeField(default=timezone.now)
    last_modify_data = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        pass


    class Meta:
        abstract = True


class Tag(BaseArticle):
    pass

class Category(BaseArticle):
    pass



class Article(BaseArticle):

    STATUS_CHOICES = (
        ('A', 'Active'),
        ('C', 'Close'),
    )

    title = models.CharField(max_length=266)
    text = models.TextField(max_length=10024)
    views = models.PositiveIntegerField(default=0)
    #image =
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    rating = GenericRelation(LikeDislike, related_query_name='article')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default='A')

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views']) # Если в save() передать update_fields, только эти поля будут обновлены.


