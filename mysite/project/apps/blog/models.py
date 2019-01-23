from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from project.apps.like_dislike.models import Like, Subscribe
from .utils import make_thumbnail

from os.path import splitext


class BaseArticle(models.Model):
    create_data = models.DateTimeField(_('Create data'), default=timezone.now)
    last_modify_data = models.DateTimeField(_('Last modify data'), default=timezone.now)
    is_active = models.BooleanField(_('Is active'), default=True)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._image_values = values[field_names.index('image')]
        return instance

    def save(self,  *args, **kwargs):
        if self.image:
            if self._state.adding or self._image_values != self.image:
                text, ex = splitext(self.image.name.lower())
                if ex != '.gif':
                    make_thumbnail(self.image, (self.max_width, self.max_height))
        super().save(*args, **kwargs)
        for hashtag in do_hashtags(self.text):
            tag, stat = Tag.objects.get_or_create(name=hashtag, defaults={'name': hashtag})
            self.tags.add(tag)


    def _save(self,  *args, **kwargs):
        super().save(*args, **kwargs)

    def _delete(self):
        self.is_active = False
        self._save(update_fields=['is_active'])

    def _return(self):
        self.is_active = True
        self._save(update_fields=['is_active'])

    class Meta:
        abstract = True

############################################################################

class TagManger(models.Manager):
    def top_tags(self):
        return self.annotate(sort=models.Count('article')).order_by('-sort')[:10]

class Tag(models.Model):
    create_data = models.DateTimeField(_('Create data'), default=timezone.now)
    name = models.CharField(_('Name'), max_length=44, unique=True)

    objects = TagManger()

    def popular(self):
        return self.article_set.count()

    def __str__(self):
        return self.name


#############################################################################


from .utils import do_hashtags

class ArticleManager(models.Manager):


    def loader(self, req, location):
        objs = self.filter(is_active=True)
        f, q = req.GET.get('f'), req.GET.get('q')
        if f:
            objs = objs.filter(**{location.field:f})
        if q:
            objs = objs.filter(text__icontains=q)
        return objs



class Article(BaseArticle):

    max_width = settings.MAX_WIDTH_IMG
    max_height = settings.MAX_HEIGHT_IMG

    text = models.TextField(_('Text'), max_length=settings.MAX_POST_SIZE,  null=True, blank=True)
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Views'), blank=True, related_name='article_set_views')
    image = models.ImageField(_('Image'), upload_to='post_img/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE)
    like = GenericRelation(Like, verbose_name=_('Like'), related_query_name='article')

    objects = ArticleManager()

    def viewed(self, user):
        if not self.views.filter(username=user.username).exists():
            self.views.add(user)

    def get_absolute_url(self):
        return reverse('account:profile-post', kwargs={'login': self.author.username, 'init': self.id})


    @property
    def get_user(self):
        return self.author

    class Meta:
        ordering = ['-id']
