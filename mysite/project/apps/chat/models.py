from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Count
from django.utils.translation import gettext as _


class DialogManager(models.Manager):

    def get_user_dialogs(self, user):
        return self.annotate(msg=Count('message')).filter(Q(from_user=user) | Q(to_user=user), msg__gte=1)

    def get_or_create_dialog(self, user1, user2):
        dialog, stat = Dialog.objects.filter(Q(from_user=user1, to_user=user2) |
                                                    Q(to_user=user1, from_user=user2)).get_or_create(
                                                    defaults={'from_user': user1, 'to_user': user2})
        return dialog, (stat * 'New') or 'old'

    def loader(self, req, location):
        return self.get_user_dialogs(req.user)


class Dialog(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('From user'),  on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='dialog_from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('To user'), on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='dialog_to_user')
    objects = DialogManager()

    def __str__(self):
        return str(self.from_user) + ' - ' + str(self.to_user)

    def auth_user(self, user):
        return self.to_user != user and self.from_user != user

    def readed(self, user):
        return self.message_set.last().readed


    class Meta:
        ordering = ['-id']



class MessageManager(models.Manager):

    def create_message(self, **kwargs):
        msg = self.create(**kwargs)
        return msg.id

    def loader(self, req, location):
        return self.filter(dialog_id=req.GET.get('f'))


class Message(models.Model):

    text = models.TextField(_('Text'), max_length=300)
    dialog = models.ForeignKey(Dialog, verbose_name=_('Dialog'), on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.SET_NULL, null=True, blank=True)
    data_publish = models.DateTimeField(_('Data publish'), default=timezone.now)
    readed = models.BooleanField(_('Readed'), default=False)

    objects = MessageManager()

    def to_(self):
        return self.dialog.from_user if self.dialog.from_user != self.author else self.dialog.to_user

    def user_readed_msg(self):
        self.readed = True
        self.save(update_fields=['readed'])
        return ''

    class Meta:
        ordering = ['-id']