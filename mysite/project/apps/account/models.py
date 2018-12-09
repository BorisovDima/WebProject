from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from project.apps.chat.models import Dialog
from django.conf import settings
from project.apps.blog.utils import make_thumbnail
from uuid import uuid4


DEFAULT_USER_IMG = 'user_img/default_user_img.png'

class BlogUser(AbstractUser):
     profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
     followers = models.ManyToManyField('self', symmetrical=False) # если я твой follower (followers.all()),
                                                                   # то ты мой Subscriber  (bloguser_set.all())
     is_verified = models.BooleanField(default=False)
     uuid = models.UUIDField(default=uuid4)
     email = models.EmailField('email', unique=True)

     rating = models.IntegerField(default=0)

     def get_absolute_url(self):
          self.profile.get_absolute_url()

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

