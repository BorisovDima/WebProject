
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class BlogUser(AbstractUser):
     avatar = models.ImageField(null=True, blank=True)
     friends = models.ManyToManyField('self', symmetrical=False)
     slug = models.SlugField(allow_unicode=True, unique=True)

     def save(self, *args, **kwargs):
          self.slug = self.username
          return super().save(*args, **kwargs)

     def get_absolute_url(self):
          pass

     def get_full_url(self):
          pass