from django.db import models
from django.utils import timezone
from django.shortcuts import render_to_response
from django.utils.translation import gettext_lazy as _

class BanList(models.Model):
    ban_24h_template = 'account/ban_24.html'
    ban_15m_template = 'account/ban_15.html'

    ban = models.BooleanField(_('Ban'), default=False)
    attempts = models.IntegerField(_('Attempts'), default=0)
    time_unblock = models.DateTimeField(_('Time unblock'), default=timezone.now)
    ip = models.GenericIPAddressField(_('ip'))

    def __str__(self):
        return 'stat-{}: attempt-{}: time-{}: {}'.format(self.ban, self.attempts, self.time_unblock, self.ip)

    def banned(self):
        self.attempts += 1
        if self.attempts in [6, 9, 12]:
            self.time_unblock = timezone.now() + timezone.timedelta(minutes=15) \
                if self.attempts in [6, 9] else timezone.now() + timezone.timedelta(hours=24)
            self.ban = True
        elif self.attempts > 12:
            self.attempts = 1
        self.save()

    def check_ban(self):
        if self.ban and timezone.now() < self.time_unblock:
            if self.attempts in [6, 9, 12]:
                template = self.ban_15m_template if self.attempts in [6, 9] else self.ban_24h_template
                return {'status': 'ban', 'response': render_to_response(template)}
        elif self.ban and timezone.now() > self.time_unblock:
            self.ban = False
            self.save(update_fields=['ban'])
        return {'status': 'ok'}

    def ban_15m(self):
        self.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
        self.save(update_fields=['time_unblock'])

    def ban_24h(self):
        self.time_unblock = timezone.now() + timezone.timedelta(hours=24)
        self.save(update_fields=['time_unblock'])


from django.contrib import admin


class BanListAdmin(admin.ModelAdmin):
    list_display = ('ip', 'ban', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)