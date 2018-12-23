from django import template
from project.apps.blog.models import Thread
from django.contrib.auth import get_user_model
register = template.Library()

@register.inclusion_tag('account/tag/user_head.html')
def head_user(status, user, profile):
    return {'user_status': status, 'user': user, 'profile': profile}

from django.utils.html import format_html
from django.utils import timezone

@register.simple_tag
def user_online(user):
    if ((timezone.now() - user.last_activity).total_seconds() // 60) < 10:
        return format_html('<a class="text-info">Online</a>')
    else:
        return format_html('<a class="text-muted">offline</a>')