from django import template


register = template.Library()

@register.inclusion_tag('tag/like.html')
def like_html(obj, type, user):
    likes = obj.like.all()
    action = likes.filter(user=user).exists() if user.is_authenticated else False
    return {'count': likes.count(), 'type': type, 'id': obj.id, 'action': action}


@register.inclusion_tag('tag/subscribe.html')
def subscribe_html(obj, type, user):
    action = obj.my_followers.filter(user=user).exists()
    return {'type': type, 'id': obj.id, 'action': action}
