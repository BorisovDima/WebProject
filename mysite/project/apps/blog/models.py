from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import LikeDislike
from django.conf import settings
from django.urls import reverse
from .utils import make_thumbnail






class BaseArticle(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    last_modify_data = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Tag(BaseArticle):
    name = models.CharField(max_length=124, unique=True, db_index=True)

from django.db.models import Count

class ThreadManager(models.Manager):

    def get_top(self):
        return self.annotate(count_community=Count('participant')).order_by('-count_community')[:21]

class Thread(BaseArticle):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    sub = models.CharField(max_length=124)
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='thread_img/', null=True, blank=True)

    objects = ThreadManager()

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('blog:thread', kwargs={'thread': self.name})

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        make_thumbnail(self.image, (settings.MAX_WIDTH_IMG-300, settings.MAX_HEIGHT_IMG-300))
        return super().save(*args, **kwargs)


class Article(BaseArticle):

    STATUS_CHOICES = (
        ('P', 'POST'),
        ('A', 'ARTICLE'),
    )

    title = models.CharField(max_length=524, null=True, blank=True)
    text = models.TextField(max_length=2024,  null=True, blank=True)
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='article_set_views')
    image = models.ImageField(upload_to='post_img/', null=True, blank=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,  null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = GenericRelation(LikeDislike, related_query_name='article')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, blank=True)
    top = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.width > settings.MAX_WIDTH_IMG or self.image.height > settings.MAX_HEIGHT_IMG:
                make_thumbnail(self.image, (settings.MAX_WIDTH_IMG, settings.MAX_HEIGHT_IMG))
        return super().save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse('blog:detail_article', kwargs={'login': self.author, 'pk': self.pk})

    def viewed(self, user):
        if not self.views.filter(username=user.username).exists():
            self.views.add(user)



    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.id)



