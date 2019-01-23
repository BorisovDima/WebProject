from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template import loader

from project.apps.account.models import BlogUser

class NotifyManager(models.Manager):

     def loader(self, req, location):
          return self.filter(owner=req.user)


class Notification(models.Model):

     C_template = None
     CP_template = None
     L_template = None
     S_template = None

     event_choice = (
          ('C', getattr(settings, 'COMMENT_NOTIFY_TEMPLATE', 'event_handler/tag/parent-comment.html')),
          ('CP', getattr(settings, 'COMMENT_POST_NOTIFY_TEMPLATE', 'event_handler/tag/comment.html')),
          ('L', getattr(settings, 'LIKE_NOTIFY_TEMPLATE', 'event_handler/tag/notify-like.html')),
          ('S', getattr(settings, 'SUBS_NOTIFY_TEMPLATE', 'event_handler/tag/notify-subs.html'))
     )

     owner = models.ForeignKey(BlogUser, verbose_name=_('Owner'), related_name='notify_owner', on_delete=models.CASCADE)
     initiator = models.ForeignKey(BlogUser, verbose_name=_('Initiator'), related_name='notify_initiator', on_delete=models.CASCADE)
     event = models.CharField(_('Event'), choices=event_choice, max_length=20)
     readed = models.BooleanField(_('Readed'), default=False)

     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
     object_id = models.PositiveIntegerField()
     content_object = GenericForeignKey('content_type', 'object_id')

     objects = NotifyManager()

     @property
     def template(self):
          return '%s_template' % self.event

     @property
     def current_template(self):
          return self.get_event_display()

     @classmethod
     def get_template_event(cls, obj, context):
          """ Easy cache """
          obj_template = obj.template
          template = getattr(cls, obj_template)
          if not template:
               setattr(cls, obj_template, loader.get_template(obj.current_template))
               template = getattr(cls, obj_template)
          return template.render(context)

     def read(self):
          self.readed = True
          self.save(update_fields=['readed'])
          return ''


     class Meta:
          ordering = ['-id']