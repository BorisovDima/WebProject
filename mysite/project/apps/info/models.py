from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.conf import settings
from django.contrib import admin

class InfoModel(models.Model):

    lang = (('ru', 'russian'),
            ('en', 'english'))

    url = models.CharField(max_length=50)
    html = models.TextField()
    language = models.CharField(choices=lang, max_length=30, default='en')

    def __str__(self):
        return '%s:(%s)' % (self.url, self.language)


class Question(models.Model):

    create_data = models.DateTimeField(_('Create data'), default=timezone.now)
    title = models.CharField(_('Question title'), max_length=100)
    body = models.CharField(_('Question body'), max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    status = models.BooleanField(_('Question open'), max_length=20, default=True)
    def __str__(self):
        return 'Question %s' % self.user.username

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user', 'create_data')
    search_fields = ('title',)