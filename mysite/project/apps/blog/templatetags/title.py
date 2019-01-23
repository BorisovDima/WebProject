from django import template

register = template.Library()

@register.simple_tag
def title(request, user):
    print(user)
    try:
        if not request.resolver_match.kwargs.get('title_user'):
            return request.resolver_match.kwargs.get('title')
        else:
            return request.resolver_match.kwargs.get('login')
    except Exception:
        return 'page'
