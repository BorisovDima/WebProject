from django import template
from project.apps.blog.models import Community, Tag
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

from project.apps.comments.forms import CommentForm
@register.inclusion_tag('tag/post.html')
def detail_post(user):
    return {'user': user, 'form_comment': CommentForm()}

@register.inclusion_tag('tag/post.html')
def home_sidebar(user):
    return {'user': user, 'form_comment': CommentForm()}

from django.template.defaultfilters import stringfilter
from project.apps.blog.utils import hashtag_pattern

from django.utils.html import conditional_escape

@register.filter(needs_autoescape=True)
@stringfilter
def hashtags(text, autoescape=True):
    text = conditional_escape(text)
    call = lambda a: '<a href="' + reverse('search:search-posts') + \
                     '?q=' + a.group(1) + '">' + a.group(0) + '</a>'
    resp = mark_safe(hashtag_pattern.sub(call, text))
    return resp

@register.inclusion_tag('tag/tags.html')
def top_tags():
    return {'tags': Tag.objects.top_tags() }


import random
from django.contrib.auth import get_user_model
from project.apps.like_dislike.models import Subscribe


@register.inclusion_tag('tag/home_sidebar.html')
def home_sidebar(user):
    users, model = [], get_user_model()
    follow = model.objects.filter(my_followers__user=user)
    for f in follow.annotate(sort=Count('my_followers')).order_by('-sort'):
        fol = Subscribe.objects.filter(user=f, type='U').exclude(object_id=user.id)
        if fol: users.append(random.choice(fol).content_object)
        if len(users) > 8:
            return {'users': users}
    location = user.profile.country
    for m in model.objects.filter(
            profile__country=location).annotate(sort=Count('my_followers')).order_by('-sort').exclude(id=user.id):
        users.append(m)
        if len(users) > 8:
            break
    return {'users': users}


from django.utils import timezone
@register.inclusion_tag('tag/edit_button.html')
def redact_post(post):
    if timezone.now() < post.create_data + timezone.timedelta(hours=24):
        return {'edit': True , 'post': post}
    return {'edit': False}



