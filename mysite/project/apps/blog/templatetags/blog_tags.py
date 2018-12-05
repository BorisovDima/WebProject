from django import template
from project.apps.blog.models import Thread
from project.apps.blog.forms import CreatePostForm, MAX_LENGTH_POST
from django.utils.text import mark_safe



register = template.Library()

@register.inclusion_tag('tag/navbar.html')
def load_navbar(user, category=None, **extra):
    threads = Thread.objects.all()
    kwargs = {'categories': threads, 'user': user, 'category': category}
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

@register.inclusion_tag('tag/form_post.html')
def post_form():
    form =  CreatePostForm()
    return {'form' : form, 'max_length': MAX_LENGTH_POST}



@register.simple_tag
def thread_part(user, thread):
    if not thread.participant.filter(username=user.username).exists():
        html = '<span class="badge badge-danger float-right"><a href="#" class="text-white">Subscribe</a></span>'
    else:
        html = '<span class="badge badge-success float-right"><a href="#" class="text-white">unsubscribe</a></span>'
    return mark_safe(html)

