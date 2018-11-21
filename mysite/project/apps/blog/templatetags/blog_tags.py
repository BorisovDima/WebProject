from django import template
from project.apps.blog.models import Category

register = template.Library()

@register.inclusion_tag('tag/navbar.html')
def load_navbar(user, category):
    categories = Category.objects.all()
    return {'categories': categories,
            'user': user, 'category': category}


