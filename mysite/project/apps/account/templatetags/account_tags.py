from django import template

register = template.Library()

@register.inclusion_tag('account/tag/user_head.html')
def head_user(status, user, profile):
    return {'user_status': status, 'user': user, 'profile': profile}