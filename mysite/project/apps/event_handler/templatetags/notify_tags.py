from django import template


register = template.Library()


@register.inclusion_tag('event_handler/tag/comment.html')
def comment(obj, user):
    try:
        from_user = obj.initiator
        comm = obj.content_object
    except Exception:
        return None
    return {'comm': comm, 'from_user': from_user, 'obj': obj, 'user': user}


@register.inclusion_tag('event_handler/tag/parent-comment.html')
def parent_comment(obj, user):
    try:
        from_user = obj.initiator
        comm = obj.content_object
        parent = comm.parent_comment
    except Exception:
        return None
    return {'comm': comm, 'from_user': from_user, 'parent': parent, 'obj': obj}



@register.inclusion_tag('event_handler/tag/notify-like.html')
def notify_like(obj, user):
    try:
        from_user = obj.initiator
        post = obj.content_object.content_object
    except Exception:
        return None
    return {'post': post, 'from_user': from_user, 'obj': obj, 'user': user}




@register.inclusion_tag('event_handler/tag/notify-subs.html')
def subs(obj, user):
    try:
        from_user = obj.initiator
    except Exception:
        return None
    return {'from_user': from_user, 'obj': obj}

