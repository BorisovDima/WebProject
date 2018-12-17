from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from project.apps.chat.models import Dialog
from django.conf import settings
from project.apps.blog.utils import make_thumbnail
from uuid import uuid4
from django.utils import timezone
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.fields import GenericRelation

DEFAULT_USER_IMG = 'user_img/default_user_img.png'

class BlogUser(AbstractUser):
     profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

     my_followers = GenericRelation(Subscribe, related_query_name='user_followers')
     is_verified = models.BooleanField(default=False)
     uuid = models.UUIDField(default=uuid4)
     email = models.EmailField('email', unique=True)
     last_verify = models.DateTimeField(default=timezone.now)

     rating = models.IntegerField(default=0)

     def get_subscribers(self):
          return self.my_followers.all()

     def get_sub_url(self):
          return reverse('account:subscribe', kwargs={'key': self.username})

     def get_absolute_url(self):
          return self.profile.get_absolute_url()

     def get_full_url(self):
          pass



class Profile(models.Model):
     login = models.SlugField(allow_unicode=True, unique=True, max_length=255)
     date_of_birth = models.DateTimeField(null=True, blank=True)
     current_city = models.CharField(max_length=99, null=True, blank=True)
     about_me = models.CharField(max_length=255, null=True, blank=True)
     user_img = models.ImageField(upload_to='user_img/', default=DEFAULT_USER_IMG)
     thumbnail = models.ImageField(upload_to='user_img/thumbnails/')

     @classmethod
     def from_db(cls, db, field_names, values):
          new = super().from_db(db, field_names, values)
          new._load_data = dict(zip(field_names, values))
          return new


     def save(self, *args, **kwargs):
          if self._state.adding or (self._load_data['user_img'] != self.user_img):
               make_thumbnail(self.user_img, (settings.MAX_WIDTH_IMG, settings.MAX_HEIGHT_IMG),
                        icon=(settings.USER_ICON, self.thumbnail))
               if not self._state.adding:
                    self.about_me = self._load_data['about_me']
          return super().save(*args, **kwargs)


     def get_user_dialogs(self):
          return Dialog.objects.get_user_dialogs(self.bloguser)


     def get_user_followers(self):
          return self.bloguser.my_followers.all()

     def get_user_subscriptions(self):
          return Subscribe.objects.filter(user=self.bloguser)

     def get_user_articles(self):
          return self.bloguser.article_set.all()

     def get_user_joined(self):
          return self.bloguser.date_joined

     def get_user_name(self):
          return False if not self.bloguser.first_name or not self.bloguser.last_name else \
               self.bloguser.first_name + ' ' + self.bloguser.last_name

     def get_absolute_url(self):
          return reverse('account:profile', kwargs={'login': self.login})

     @property
     def pref_name(self):
          return '@' + self.login


     class Meta:
          ordering = ['-id']


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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