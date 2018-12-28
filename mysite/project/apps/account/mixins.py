from django.http import JsonResponse
from django.shortcuts import redirect
from project.apps.myauth.utils import check_google_captcha

class NotLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)




class AjaxMixin:
    captcha = None

    def form_invalid(self, form, captcha=None):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            errors = form.errors if not captcha else {'captcha': 'Captcha error. Please try again'}
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