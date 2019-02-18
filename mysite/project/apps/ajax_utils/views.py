from django.http import JsonResponse
from django.views.generic import View
from django.template.loader import render_to_string

from .mixins import AjaxLoaderMixin


class AjaxLoaderView(AjaxLoaderMixin, View):
    model = None
    template_name = None

    def get(self, req, *args, **kwargs):
        objs, since = self.get_data(req)
        if not objs: return JsonResponse({'status': 'end'})
        button = len(objs) > self.location.paginate
        return JsonResponse({'html': render_to_string(self.template_name, {'objs': objs}, self.request),
                             'since': since,
                             'button': button,
                             'status': 'ok'})



