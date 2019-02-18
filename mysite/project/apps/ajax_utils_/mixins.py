from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from project.apps.myauth.utils import check_google_captcha


class AjaxMixin:
    captcha = None


    def get_json(self, request, extra=None, **kwargs):
        response = {'html': render_to_string(self.template_name, kwargs, request)}
        if extra:
            response.update(extra)
        return JsonResponse(response)


    def form_invalid(self, form, captcha=None):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            errors = form.errors if not captcha else {'captcha': _('Captcha error. Please try again')}
            return JsonResponse(errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            if self.captcha and not check_google_captcha(self.request):
                return self.form_invalid(form, captcha=True)
            return JsonResponse(self.get_data(form))
        else:
            return response