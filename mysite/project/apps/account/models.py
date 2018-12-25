from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from project.apps.chat.models import Dialog
from uuid import uuid4
from django.utils import timezone
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.fields import GenericRelation
from project.apps.blog.models import Community
from django.contrib.contenttypes.models import ContentType



class BlogUser(AbstractUser):

     my_followers = GenericRelation(Subscribe, related_query_name='user_followers')
     is_verified = models.BooleanField(default=False)
     uuid = models.UUIDField(default=uuid4)
     email = models.EmailField('email', unique=True, blank=False, null=False)
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
     bloguser = models.OneToOneField(BlogUser, on_delete=models.CASCADE)

     user_name = models.CharField(max_length=40, null=True, blank=True)
     name = models.SlugField(allow_unicode=True, unique=True, max_length=255)
     date_of_birth = models.DateTimeField(null=True, blank=True)
     current_city = models.CharField(max_length=99, null=True, blank=True)
     about_me = models.CharField(max_length=120, null=True, blank=True)
     image = models.ImageField(upload_to='user_img/', null=True, blank=True)
     thumbnail = models.ImageField(upload_to='user_img/thumbnails/', null=True, blank=True)
     head = models.ImageField(upload_to='user_img/', null=True, blank=True)

     def get_user_dialogs(self):
          return Dialog.objects.get_user_dialogs(self.bloguser)


     def get_user_followers(self):
          return self.bloguser.my_followers.all()

     def get_user_community_sub(self):
          return Subscribe.objects.filter(user=self.bloguser, content_type=ContentType.objects.get_for_model(Community))

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

from django.utils import timezone
from django.shortcuts import render_to_response


class BanList(models.Model):
     ban_24h_template = 'account/ban_24.html'
     ban_15m_template = 'account/ban_15.html'

     ban = models.BooleanField(default=False)
     attempts = models.IntegerField(default=0)
     time_unblock = models.DateTimeField(default=timezone.now)
     ip = models.GenericIPAddressField()

     def __str__(self):
          return 'stat-{}: attempt-{}: time-{}: {}'.format(self.ban, self.attempts, self.time_unblock, self.ip)

     def banned(self):
          self.attempts += 1
          if self.attempts in [3,6,9]:
               self.time_unblock = timezone.now() + timezone.timedelta(minutes=15) \
                    if self.attempts in [3,6] \
                    else timezone.now() + timezone.timedelta(hours=24)
               self.ban = True
          elif self.attempts > 9:
               self.attempts = 1
          self.save()

     def check_ban(self):
          if self.ban and timezone.now() < self.time_unblock:
               if self.attempts in [3,6,9]:
                    template = self.ban_15m_template if self.attempts in [3,6] else self.ban_24h_template
                    return {'status': 'ban', 'response': render_to_response(template)}
          elif self.ban and timezone.now() > self.time_unblock:
               self.ban = False
               self.save(update_fields=['ban'])
          return {'status': 'ok'}

     def ban_15m(self):
          self.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
          self.save(update_fields=['time_unblock'])

     def ban_24h(self):
          self.time_unblock = timezone.now() + timezone.timedelta(hours=24)
          self.save(update_fields=['time_unblock'])