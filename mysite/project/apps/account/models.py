from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.conf import settings
from django_countries.fields import CountryField

from project.apps.like_dislike.models import Subscribe
from project.apps.chat.models import Dialog

from uuid import uuid4
from itertools import dropwhile



class Profile(models.Model):
     bloguser = models.OneToOneField('BlogUser', verbose_name=_('User'), on_delete=models.CASCADE)

     user_name = models.CharField(_('User name'), max_length=40, null=True, blank=True)
     name = models.SlugField(_('Name'), allow_unicode=True, unique=True, max_length=255)
     date_of_birth = models.DateTimeField(_('Date of birth'), null=True, blank=True)
     country = CountryField(_('Country'), null=True, blank=True)
     about_me = models.CharField(_('About me'), max_length=120, null=True, blank=True)
     image = models.ImageField(_('Image'), upload_to='user_img/', null=True, blank=True,
                               help_text=_('You can upload an image in JPG or PNG formats. Max size file 2mb'))

     thumbnail = models.ImageField(_('Thumbnail'), upload_to='user_img/thumbnails/', null=True, blank=True)

     head = models.ImageField(_('Head'), upload_to='user_img/',
                              help_text=_('You can upload an image in JPG or PNG formats. Max size file 2mb'), null=True, blank=True)

     def get_user_dialogs(self):
          return Dialog.objects.get_user_dialogs(self.bloguser)

     def get_user_not_read_msgs(self):
          last_msgs = (dialog.message_set.first() for dialog in self.get_user_dialogs())
          return [msg for msg in last_msgs if not msg.readed and msg.to_() == self.bloguser]

     def get_user_followers(self):
          return self.bloguser.my_followers.all()

     def get_user_people_sub(self):
          return Subscribe.objects.filter(user=self.bloguser, content_type=ContentType.objects.get_for_model(BlogUser))

     def get_user_articles(self):
          return self.bloguser.article_set.all()

     def get_user_joined(self):
         data = self.bloguser.date_joined.__format__('%B %Y')
         return data

     def get_user_birth(self):
         return self.date_of_birth.__format__('%Y %B %d')


     def get_user_name(self):
               return '@' + self.bloguser.username if not self.user_name else self.user_name


     def get_absolute_url(self):
          return reverse('account:profile', kwargs={'login': self.name})

     @property
     def pref_name(self):
          return '@' + self.name

     @property
     def get_user(self):
          return self.bloguser

     class Meta:
          ordering = ['-id']




class BlogUserManager(UserManager):

     def create_user(self, username, is_verified=False, email=None, password=None):
         user = super().create_user(username, email, password, is_verified=is_verified)
         Profile.objects.create(name=user.username, bloguser=user)
         return user

     def create_superuser(self, username, email, password, is_verified=True):
          super_user = super().create_superuser(username, email, password, is_verified=is_verified)
          Profile.objects.create(name=super_user.username, bloguser=super_user)
          return super_user


     def loader(self, req, location):
          objs = self.all()
          f, q = req.GET.get('f'), req.GET.get('q')
          if f:
               objs = objs.filter(**{location.field:f})
          if q:
               objs = objs.filter(models.Q(username__icontains=q) | models.Q(profile__user_name__icontains=q))
          return objs



class BlogUser(AbstractUser):

     my_followers = GenericRelation(Subscribe, verbose_name=_('Followers'), related_query_name='user_followers')
     is_verified = models.BooleanField(_('Is verified'), default=False)
     uuid = models.UUIDField(_('Uuid'), default=uuid4)
     email = models.EmailField(_('Email'),  blank=True, null=True)
     last_activity = models.DateTimeField(_('Last activity'), default=timezone.now)
     geo = models.CharField(_('User geo'), max_length=100, default=settings.DEFAULT_GEO)

     objects = BlogUserManager()

     def get_subscribers(self):
          return self.my_followers.all()

     def get_sub_url(self):
          return reverse('account:subscribe', kwargs={'key': self.username})

     def get_absolute_url(self):
          return self.profile.get_absolute_url()


     class Meta:
          ordering = ['-id']


