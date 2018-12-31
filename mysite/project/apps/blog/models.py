from django.db import models, IntegrityError
from django.utils import timezone
from project.apps.like_dislike.models import Like, Subscribe
from django.conf import settings
from django.urls import reverse
from .utils import make_thumbnail
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.fields import GenericRelation
from os.path import splitext


class BaseArticle(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    last_modify_data = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def _save(self,  *args, **kwargs):
        return super().save(*args, **kwargs)


    def save(self,  *args, **kwargs):
        if self.image:
            text, ex = splitext(self.image.name.lower())
            print(ex)
            if ex != '.gif':
                print('NE GIF')
                make_thumbnail(self.image, (self.max_width, self.max_height))
        return super().save(*args, **kwargs)


    def _delete(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def _return(self):
        self.is_active = True
        self.save(update_fields=['is_active'])


    class Meta:
        abstract = True


class TagManger(models.Manager):

    def top_tags(self):
        return self.annotate(sort=models.Count('article')).order_by('-sort')[:10]


class Tag(models.Model):
    create_data = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=44, unique=True)

    objects = TagManger()

    def popular(self):
        return self.article_set.count()

    def __str__(self):
        return self.name


class CommunityManager(models.Manager):
    pass

class Community(BaseArticle):

    max_width = settings.MAX_WIDTH_IMG-400
    max_height = settings.MAX_HEIGHT_IMG-400

    name = models.CharField(max_length=30, unique=True, db_index=True)
    sub = models.CharField(max_length=124)
    image = models.ImageField(upload_to='community_img/', default=settings.DEFAULT_COMMUNITY_IMG)
    my_followers = GenericRelation(Subscribe, related_query_name='community_followers')

    objects = CommunityManager()

    def __str__(self):
        return str(self.name)

    def get_sub_url(self):
        return reverse('blog:subscribe-community', kwargs={'key': self.name})

    def get_absolute_url(self):
        return reverse('blog:community', kwargs={'slug': self.name})

    def get_hot(self):
        return self.my_followers.all().count() * 0.25

    def get_subscribers(self):
        return self.my_followers.all()

    class Meta:
        ordering = ['-id']


class ArticleManager(models.Manager):

    def get_last_rating(self):
        return self.order_by('-rating').last()


from .utils import do_hashtags


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
    community = models.ForeignKey(Community, on_delete=models.CASCADE,  null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = GenericRelation(Like, related_query_name='article')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, blank=True, default='P')

    objects = ArticleManager()

    def viewed(self, user):
        if not self.views.filter(username=user.username).exists():
            self.views.add(user)

    def set_tags(self):
        if self.text:
            for hashtag in do_hashtags(self.text):
                tag, stat = Tag.objects.get_or_create(name=hashtag, defaults={'name': hashtag})
                self.tags.add(tag)


    class Meta:
        ordering = ['-id']




