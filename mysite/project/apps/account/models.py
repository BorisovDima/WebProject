
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class BlogUser(AbstractUser):
     pass

     def get_absolute_url(self):
          pass

     def get_full_url(self):
          pass