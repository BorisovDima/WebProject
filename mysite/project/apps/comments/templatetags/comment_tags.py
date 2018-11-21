from django import template


register = template.Library()

@register.inclusion_tag('tag/comments.html')
def load_comments(user, article):
    comments = article.comment_set.all()
    return {'user': user, 'comments': comments}

