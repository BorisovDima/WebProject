from django.db import models
from django.conf import settings
from django.utils import timezone
from django.http.response import Http404
from django.db.models import Q



class DialogManager(models.Manager):

    def get_user_dialogs(self, user):
        return self.filter(Q(from_user=user) | Q(to_user=user))

    def get_or_create_dialog(self, user1, user2):
        dialog, stat = Dialog.objects.filter(Q(from_user=user1, to_user=user2) |
                                                    Q(to_user=user1, from_user=user2)).get_or_create(
                                                    defaults={'from_user': user1, 'to_user': user2})
        return dialog, (stat * 'New') or 'old'



class Dialog(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='dialog_from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='dialog_to_user')
    objects = DialogManager()

    def __str__(self):
        return str(self.from_user) + ' - ' + str(self.to_user)

    def auth_user(self, user):
        if self.to_user != user and self.from_user != user:
            raise Http404

    def readed(self, user):
        return self.message_set.last().readed


    class Meta:
        ordering = ['-id']


class MessageManager(models.Manager):

    def create_message(self, **kwargs):
        msg = self.create(**kwargs)
        return msg.to_(), msg.id


class Message(models.Model):
    text = models.TextField(max_length=300)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_publish = models.DateTimeField(default=timezone.now)
    readed = models.BooleanField(default=False)

    objects = MessageManager()

    def to_(self):
        return self.dialog.from_user if self.dialog.from_user != self.author else self.dialog.to_user

    def user_readed_msg(self):
        self.readed = True
        self.save()
        return ''

