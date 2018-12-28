from django import template


register = template.Library()

@register.inclusion_tag('tag/comments.html')
def load_comments(user, article):
    comments = article.comment_set.all()
    return {'user': user, 'objs': comments}


@register.inclusion_tag('comments/comment.html')
def get_comment(comment, user, initial=''):
    context = {'initial': initial}
    if comment.parent_comment:
        context['parent_id'] = comment.parent_comment.id
        context['parent_active'] = comment.parent_comment.is_active
        if comment.parent_comment.author:
            context['parent_profile'] = comment.parent_comment.author.profile
            context['parent_name'] = comment.parent_comment.author.username
    context['create_data'] = comment.create_data
    context['text'] = comment.text
    context['comment_id'] = comment.id
    if comment.author:
        context['author_profile'] = comment.author.profile
        context['author'] = comment.author.username
        context['del'] = (comment.author == user)
    context['user'] = user
    return context

@register.inclusion_tag('comments/child_comments.html')
def get_comment_child(comment, user):
    child = comment.initial_comment_set.filter(is_active=True).last()
    count = comment.initial_comment_set.count()
    next = count > 1
    return {'child': child, 'user': user, 'initial': comment.id, 'next': next, 'count': count}