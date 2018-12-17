from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import Like, Subscribe
from django.conf import settings
from django.urls import reverse
from .utils import make_thumbnail
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.fields import GenericRelation

class BaseArticle(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    last_modify_data = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def _save(self,  *args, **kwargs):
        return super().save(*args, **kwargs)


    def save(self,  *args, **kwargs):
        if self.image:
            make_thumbnail(self.image, (self.max_width, self.max_height))
        return super().save(*args, **kwargs)


    def _delete(self):
        self.active = False
        self.save(update_fields=['active'])

    def _return(self):
        self.active = True
        self.save(update_fields=['active'])


    class Meta:
        abstract = True



class Tag(BaseArticle):
    name = models.CharField(max_length=124, unique=True, db_index=True)




class ThreadManager(models.Manager):
    pass

class Thread(BaseArticle):

    max_width = settings.MAX_WIDTH_IMG-400
    max_height = settings.MAX_HEIGHT_IMG-400


    name = models.CharField(max_length=30, unique=True, db_index=True)
    sub = models.CharField(max_length=124)
    image = models.ImageField(upload_to='thread_img/', default=settings.DEFAULT_COMMUNITY_IMG)
    my_followers = GenericRelation(Subscribe, related_query_name='thread_followers')
    objects = ThreadManager()

    def __str__(self):
        return str(self.name)

    def get_sub_url(self):
        return reverse('blog:subscribe-thread', kwargs={'key': self.name})

    def get_absolute_url(self):
        return reverse('blog:thread', kwargs={'thread': self.name})

    def get_hot(self):
        return self.my_followers.all().count() * 0.25

    def get_subscribers(self):
        return self.my_followers.all()

    class Meta:
        ordering = ['-id']


class ArticleManager(models.Manager):

    def get_last_rating(self):
        return self.order_by('-rating').last()

class Article(BaseArticle):

    max_width = settings.MAX_WIDTH_IMG
    max_height = settings.MAX_HEIGHT_IMG

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
    like = GenericRelation(Like, related_query_name='article')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, blank=True)

    objects = ArticleManager()

    def get_absolute_url(self):
        return reverse('blog:detail_article', kwargs={'login': self.author, 'pk': self.pk})

    def viewed(self, user):
        if not self.views.filter(username=user.username).exists():
            self.views.add(user)


    class Meta:
        ordering = ['-id']




