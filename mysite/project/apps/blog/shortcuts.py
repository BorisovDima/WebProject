from django.template import loader

def render_to_html(path, context, request=None):
    template = loader.get_template(path)
    return template.render(context, request) if request else template.render(context)