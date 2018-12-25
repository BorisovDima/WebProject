from django import template
from project.apps.blog.models import Community
from project.apps.blog.forms import CreatePostForm, MAX_LENGTH_POST
from django.utils.text import mark_safe
from django.urls import reverse
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('tag/navbar.html')
def load_navbar(user, category=None, **extra):
    communities = Community.objects.all()
    kwargs = {'categories': communities, 'user': user, 'category': category}
    kwargs.update(extra)
    return kwargs

@register.simple_tag
def msg_count(user, id_dialog=None):
    dialogs = user.profile.get_user_dialogs()
    count = 0
    for dialog in dialogs:
        last_msg = dialog.message_set.last()
        if not last_msg: continue
        if last_msg.to_() == user and not last_msg.readed and dialog.id != id_dialog: count += 1
    return count or ''


from project.apps.event_handler.models import Notification

@register.simple_tag
def notify_count(user):
    return Notification.objects.filter(owner=user).filter(readed=False).count() or ''

@register.inclusion_tag('tag/form_post.html')
def post_form(community=None):
    form = CreatePostForm() if not community else CreatePostForm(initial={'community': community})
    return {'form' : form, 'max_length': MAX_LENGTH_POST, 'community': community}

@register.inclusion_tag('tag/communities-sidebar.html')
def top_communities(user):
    communities = Community.objects.annotate(com=Count('my_followers')).order_by('-com')[:6]
    return {'tops': communities, 'user': user}


@register.inclusion_tag('tag/modal-dialogs.html')
def my_messages(user):
    return {'user': user}

@register.inclusion_tag('tag/modal-notify.html')
def my_notify(user):
    return {'user': user}

@register.simple_tag
def count_comments(obj):
    return obj.comment_set.filter(is_active=True).count()
