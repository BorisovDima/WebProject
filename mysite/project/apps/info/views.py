from django.views.generic import TemplateView, CreateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.text import mark_safe
from django.template.loader import render_to_string
from django.conf import settings

from project.apps.blog.mixins import CacheMixin
from .models import InfoModel
from project.apps.ajax_utils_.mixins import AjaxMixin
from project.apps.myauth.utils import check_google_captcha
from project.apps.back_task.tasks import sendler_mail


class Info(CacheMixin, TemplateView):
    model = InfoModel

    def get(self, request, **kwargs):
        try:
            obj = self.model.objects.get(url=kwargs['url'], language=request.LANGUAGE_CODE)
        except self.model.DoesNotExist:
            obj = get_object_or_404(self.model, url=kwargs['url'], language=settings.LANGUAGE_CODE)
        return JsonResponse({'html': mark_safe(obj.html)}) if request.is_ajax() else super().get(request, **kwargs)



class QuestionView(AjaxMixin, CreateView):
    template_name_success = 'info/success.html'
    success_url = '/info/support/'

    def get(self, req, **kwargs):
        return self.get_json(req, form=self.get_form())

    def get_data(self, form):
        return {'html': render_to_string(self.template_name_success, {'type': self.kwargs['type']}, self.request)}

    def send_email(self, email, title, body):
        body += ' ' + email
        sendler_mail.delay(title, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])


    def form_valid(self, form):
        if self.kwargs.get('type') == 'email':
            if not check_google_captcha(self.request):
                return self.form_invalid(form, captcha=True)
            self.send_email(form.cleaned_data['email'], form.cleaned_data['title'], form.cleaned_data['body'])
            return JsonResponse(self.get_data(form))
        form.instance.user = self.request.user
        return super().form_valid(form)


