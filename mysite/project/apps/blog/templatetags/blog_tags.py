from django import template
from django.utils.text import mark_safe
from django.urls import reverse
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape

from project.apps.blog.utils import hashtag_pattern
from project.apps.blog.models import Tag
from project.apps.blog.forms import CreatePostForm
from project.apps.event_handler.models import Notification
from project.apps.account.utils import get_user_recommends
from project.apps.comments.forms import CommentForm

register = template.Library()

@register.inclusion_tag('tag/navbar.html')
def load_navbar(user, **kwargs):
    print(kwargs)
    kwargs.update({'user': user})
    return kwargs

@register.simple_tag
def msg_count(user, id_dialog=None):
    count = len(user.profile.get_user_not_read_msgs())
    return count or ''


@register.simple_tag
def notify_count(user):
    return Notification.objects.filter(owner=user).filter(readed=False).count() or ''

@register.inclusion_tag('tag/form_post.html')
def post_form():
    form = CreatePostForm()
    return {'form' : form, 'max_length': settings.MAX_POST_SIZE}

@register.inclusion_tag('tag/modal-notify.html')
def my_notify(user):
    return {'user': user}


@register.simple_tag
def count_comments(obj):
    return obj.comment_set.filter(is_active=True).count()


@register.inclusion_tag('tag/post.html')
def detail_post(user):
    return {'user': user, 'form_comment': CommentForm()}




@register.filter(needs_autoescape=True)
@stringfilter
def hashtags(text, autoescape=True):
    text = conditional_escape(text)
    call = lambda a: '<a href="' + reverse('search:search') + \
                     '?q=' + a.group(1) + '">' + a.group(0) + '</a>'
    resp = mark_safe(hashtag_pattern.sub(call, text))
    return resp

@register.inclusion_tag('tag/tags.html')
def top_tags():
    return {'tags': Tag.objects.top_tags()}



@register.inclusion_tag('tag/home_sidebar.html')
def home_sidebar(user, request, count=5):
    return get_user_recommends(user, request, count)


from django.utils import timezone
@register.inclusion_tag('tag/edit_button.html')
def redact_post(post):
    if timezone.now() < post.create_data + timezone.timedelta(hours=24):
        return {'edit': True , 'post': post}
    return {'edit': False}

@register.inclusion_tag('tag/about-sidebar.html')
def about():
    return {}
