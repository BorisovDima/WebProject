from django import template
from django.utils.safestring import mark_safe
from project.apps.blog.models import Category

register = template.Library()

@register.inclusion_tag('blog/Category.html')
def show_category(category):
    categories = Category.objects.all()
    return {'categories': categories}


