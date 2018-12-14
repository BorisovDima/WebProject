from django import template


register = template.Library()

@register.inclusion_tag('tag/like.html')
def like_html(obj, type):
    likes = obj.like.all().count()
    return {'count':likes, 'type': type, 'id': obj.id}


@register.inclusion_tag('tag/subscribe.html')
def subscribe_html(obj, type, user):
    action = obj.my_followers.filter(user=user).exists()
    return {'type': type, 'id': obj.id, 'action': action}
