from django.template import Library

register = Library()

@register.simple_tag
def load_notify_template(obj):
    try:
        context = {'obj': obj}
        template = obj.get_template_event(obj, context)
    except Exception as i:
        print(i)
        ## logger ##
        template = ''
    return template