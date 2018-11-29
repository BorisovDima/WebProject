from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from project.apps.chat.models import Dialog


class BlogUser(AbstractUser):
     profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
     friends = models.ManyToManyField('self') # если я тебе друг, то и ты мне друг
     followers = models.ManyToManyField('self', symmetrical=False) # если я твой follower (followers.all()),
                                                                   # то ты мой Subscriber  (bloguser_set.all())



     def get_absolute_url(self):
          pass

     def get_full_url(self):
          pass


class Profile(models.Model):
     login = models.SlugField(allow_unicode=True, unique=True, max_length=255)
     avatar = models.ImageField(null=True, blank=True)
     date_of_birth = models.DateTimeField(null=True, blank=True)
     current_city = models.CharField(max_length=99, null=True, blank=True)
     about_me = models.CharField(max_length=255, null=True, blank=True)


     def get_user_dialogs(self):
          return Dialog.objects.get_user_dialogs(self.bloguser)


     def get_user_friends(self):
          return self.bloguser.friends.all()


     def get_user_followers(self):
          return self.bloguser.followers.all()

     def get_user_subscriptions(self):
          return self.bloguser.bloguser_set.all()

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


