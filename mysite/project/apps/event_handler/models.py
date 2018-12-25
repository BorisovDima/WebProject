from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from project.apps.account.models import BlogUser

class Notification(models.Model):

     event_choice = (
          ('C', 'comment'),
          ('CP', 'comment-post'),
          ('L', 'like'),
          ('S', 'subscription')
     )


     owner = models.ForeignKey(BlogUser, related_name='notify_owner', on_delete=models.CASCADE)
     initiator = models.ForeignKey(BlogUser, related_name='notify_initiator', on_delete=models.CASCADE)
     event = models.CharField(choices=event_choice, max_length=20)
     readed = models.BooleanField(default=False)

     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
     object_id = models.PositiveIntegerField()
     content_object = GenericForeignKey('content_type', 'object_id')

     def read(self):
          self.readed = True
          self.save(update_fields=['readed'])
          return ''

     class Meta:
          ordering = ['-id']