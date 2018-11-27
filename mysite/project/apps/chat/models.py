from django.db import models
from django.conf import settings
from django.utils import timezone

class Dialog(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='dialog_from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='dialog_to_user')

    def __str__(self):
        return str(self.from_user) + ' - ' + str(self.to_user)



class MessageManager(models.Manager):

    def create_message(self, **kwargs):
        self.create(**kwargs)

class Message(models.Model):
    text = models.TextField(max_length=500)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_publish = models.DateTimeField(default=timezone.now)
    readed = models.BooleanField(default=False)

    objects = MessageManager()

    def to_(self):
        return self.dialog.from_user if self.dialog.from_user != self.author else self.dialog.to_user



