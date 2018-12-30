from django import template
from project.apps.comments.models import Comment

register = template.Library()

@register.inclusion_tag('tag/comments.html')
def load_comments(user, article):
    comments = article.comment_set.all()
    return {'user': user, 'objs': comments}

def get_context(comment, user, initial):
    print(comment, initial)
    context = {'initial': initial}
    if comment.parent_comment:
        context['parent_id'] = comment.parent_comment.id
    context['create_data'] = comment.create_data
    context['text'] = comment.text
    context['comment_id'] = comment.id
    context['author'] = comment.author.username
    context['del'] = (comment.author == user)
    context['user'] = user
    context['is_active'] = comment.is_active
    return context

@register.inclusion_tag('comments/comment.html')
def get_comment(comment, user, initial=''):
    return get_context(comment, user, initial)

@register.inclusion_tag('comments/child_comments.html')
def get_comment_child(comment, user):
    child = comment.initial_comment_set.filter(is_active=True)
    count = child.count()
    child = child.last()
    next = count > 1
    return {'child': child, 'user': user, 'initial': comment.id, 'next': next, 'count': count}


@register.inclusion_tag('tag/comm_img.html')
def get_comm_img(author, parent=None):
    author = Comment.objects.get(id=author)
    if parent:
        parent = Comment.objects.get(id=parent)
    return {'author': author, 'parent': parent}