from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from project.apps.chat.models import Dialog
from uuid import uuid4
from django.utils import timezone
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.blog.models import Thread
from django.contrib.contenttypes.models import ContentType

DEFAULT_USER_IMG = 'user_img/default_user_img.png'

class BlogUser(AbstractUser):
     profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

     my_followers = GenericRelation(Subscribe, related_query_name='user_followers')
     is_verified = models.BooleanField(default=False)
     uuid = models.UUIDField(default=uuid4)
     email = models.EmailField('email', unique=True)
     last_activity = models.DateTimeField(default=timezone.now)

     def get_subscribers(self):
          return self.my_followers.all()

     def get_sub_url(self):
          return reverse('account:subscribe', kwargs={'key': self.username})

     def get_absolute_url(self):
          return self.profile.get_absolute_url()

     def get_full_url(self):
          pass

     class Meta:
          ordering = ['-id']


class Profile(models.Model):
     user_name = models.CharField(max_length=40, null=True, blank=True)
     name = models.SlugField(allow_unicode=True, unique=True, max_length=255)
     date_of_birth = models.DateTimeField(null=True, blank=True)
     current_city = models.CharField(max_length=99, null=True, blank=True)
     about_me = models.CharField(max_length=120, null=True, blank=True)
     image = models.ImageField(upload_to='user_img/', default=DEFAULT_USER_IMG)
     thumbnail = models.ImageField(upload_to='user_img/thumbnails/')
     head = models.ImageField(upload_to='user_img/', null=True, blank=True)

     def get_user_dialogs(self):
          return Dialog.objects.get_user_dialogs(self.bloguser)


     def get_user_followers(self):
          return self.bloguser.my_followers.all()

     def get_user_community_sub(self):
          return Subscribe.objects.filter(user=self.bloguser, content_type=ContentType.objects.get_for_model(Thread))

     def get_user_people_sub(self):
          return Subscribe.objects.filter(user=self.bloguser, content_type=ContentType.objects.get_for_model(BlogUser))

     def get_user_articles(self):
          return self.bloguser.article_set.all()

     def get_user_joined(self):
          return self.bloguser.date_joined

     def get_user_name(self):
          return self.user_name

     def get_absolute_url(self):
          return reverse('account:profile', kwargs={'login': self.name})

     @property
     def pref_name(self):
          return '@' + self.name


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