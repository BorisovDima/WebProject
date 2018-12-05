from django import template



register = template.Library()


@register.simple_tag
def color_dialog(author, user, readed):
    if author == user:
        return '#ffffff'
    elif readed == True:
        return '#ffffff'
    else:
        return '#e3e7ed'

