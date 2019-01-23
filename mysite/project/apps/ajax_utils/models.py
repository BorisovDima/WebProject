from django.db import models


class AjaxLoaderModel(models.Model):

    location = models.CharField(max_length=120, unique=True)
    sort = models.CharField(max_length=30)
    top_field = models.CharField(max_length=30, null=True, blank=True)
    field = models.CharField(max_length=120, null=True, blank=True)
    detail = models.BooleanField(default=False)
    type = models.CharField(max_length=120)
    paginate = models.IntegerField(default=10)


    def __str__(self):
        return self.location
