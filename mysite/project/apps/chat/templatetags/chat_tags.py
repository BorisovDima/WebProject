from django import template
from django.contrib.auth import get_user_model


register = template.Library()


@register.simple_tag
def color_dialog(author, user, readed):
    if author == user:
        return '#ffffff'
    elif readed == True:
        return '#ffffff'
    else:
        return '#f4f2f9'


@register.inclusion_tag('chat/user_img.html')
def chat_image(from_, to=None, data=None):
    from_ = get_user_model().objects.get(username=from_).profile
    if to: to = get_user_model().objects.get(username=to).profile
    return {'from': from_, 'to': to, 'data': data}
