from django.db import models
from project.apps.blog.models import BaseArticle, Article
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.like_dislike.models import Like
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class MyManager(models.Manager):

    def add_comment(self, **kwargs):
        obj = self.create(**kwargs)
        return obj.id

    def loader(self, req, location):
        return self.filter(**{location.field: req.GET.get('f')}, initial_comment=None)

class Comment(models.Model):
    create_data = models.DateTimeField(_('Create data'), default=timezone.now)
    text = models.TextField(_('Text'), max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.CASCADE,
                               blank=True, null=True)
    article = models.ForeignKey(Article, verbose_name=_('Article'), on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name=_('Parent comment'), on_delete=models.CASCADE,
                                       blank=True, null=True)
    like = GenericRelation(Like, verbose_name=_('Like'), related_query_name='Comment')
    is_active = models.BooleanField(_('Is active'), default=True)
    initial_comment = models.ForeignKey('self', verbose_name=_('Initial comment'), on_delete=models.CASCADE, related_name='initial_comment_set'
                                         ,blank=True, null=True)

    objects = MyManager()


    @property
    def get_user(self):
        return self.author

    def _delete(self, *args, **kwargs):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def _return(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    def check_child(self):
        return self.initial_comment_set.filter(is_active=True).count() > 0

    class Meta:
        ordering = ['-id']

    #def get_absolute_url(self):
        #return 'comment-' + str(self.id)


