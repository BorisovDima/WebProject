from django.template import loader

def render_to_html(request, path, context):
    template = loader.get_template(path)
    return template.render(context, request)