from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import LikeDislike
from django.conf import settings
from django.urls import reverse

class BaseArticle(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    last_modify_data = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Tag(BaseArticle):
    name = models.CharField(max_length=124, unique=True, db_index=True)



class Category(BaseArticle):
    name = models.CharField(max_length=124, unique=True, db_index=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'category': self.name})




class Article(BaseArticle):

    STATUS_CHOICES = (
        ('A', 'Active'),
        ('C', 'Close'),
    )

    title = models.CharField(max_length=524)
    text = models.TextField(max_length=2024,  null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    #image =
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rating = GenericRelation(LikeDislike, related_query_name='article')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default='A')
    slug = models.SlugField(max_length=70, unique=True)


    def save(self, *args, **kwargs):
        from .utils import slug_generate
        self.slug = slug_generate(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail_article', kwargs={'category': self.category, 'slug': self.slug})

    def viewed(self):
        self.views += 1
        super().save(update_fields=['views']) #Если в save() передать update_fields, только эти поля будут обновлены.

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.category)



