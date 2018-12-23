from django import template


register = template.Library()

@register.inclusion_tag('tag/comments.html')
def load_comments(user, article):
    comments = article.comment_set.all()
    return {'user': user, 'objs': comments}


@register.inclusion_tag('comments/comment.html')
def get_comment(comment, user):
    context = {}
    if comment.parent_comment:
        context['parent_id'] = comment.parent_comment.id
        context['parent_active'] = comment.parent_comment.is_active
        if comment.parent_comment.author:
            context['parent_name'] = comment.parent_comment.author.username
    context['create_data'] = comment.create_data
    context['text'] = comment.text
    context['comment_id'] = comment.id
    if comment.author:
        context['author'] = comment.author.username
        context['del'] = comment.author == user
    context['user'] = user
    return context

