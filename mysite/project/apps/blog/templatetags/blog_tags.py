from django import template
from project.apps.blog.models import Category


register = template.Library()

@register.inclusion_tag('tag/navbar.html')
def load_navbar(user, category=None, **extra):
    categories = Category.objects.all()
    kwargs = {'categories': categories, 'user': user, 'category': category}
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




