from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import CreateView, RedirectView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from project.apps.account.mixins import NotLoginRequiredMixin
from project.apps.ajax_utils_.mixins import AjaxMixin
from .models import BanList
from .forms import MyRegForm
from .utils import handler_ip, set_geo
from project.apps.back_task.tasks import sendler_mail


@method_decorator(require_POST, name='dispatch')
class Registr(NotLoginRequiredMixin, AjaxMixin, CreateView):
    captcha = True

    def get_data(self, form):
        return {'html': render_to_string('myauth/verify.html', {'user': form.instance.username,
                                                                            'mail': form.instance.email})}


class Login(NotLoginRequiredMixin, LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_form'] = MyRegForm()
        return context

    def post(self, req, *args, **kwargs):
        self.ip = handler_ip(req)
        self.ban_list, created = BanList.objects.get_or_create(ip=self.ip, defaults={'ip': self.ip})
        status = self.ban_list.check_ban()
        return super().post(req, *args, **kwargs) if status['status'] == 'ok' else status['response']

    def form_valid(self, form):
        self.ban_list.delete()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.ban_list.banned()
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('account:profile', kwargs={'login': self.request.user.username})


class Logout(LogoutView): pass


class Vertify_account(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(get_user_model(), uuid=self.kwargs['uuid'], is_verified=False)
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        set_geo(user, self.request)
        self.url = reverse('myauth:login')
        return super().get_redirect_url(*args, **kwargs)



@method_decorator(require_POST, name='dispatch')
class ResetPass(AjaxMixin, PasswordResetView):
    def get_data(self, form):
        return {'html': render_to_string('myauth/reset_pass.html', {'email': form.cleaned_data['email']})}

from django.views.generic import FormView


class HelpLogin(NotLoginRequiredMixin, AjaxMixin, FormView):
    captcha = True

    def get_data(self, form):
        return {'email': form.cleaned_data['email']}

    def form_valid(self, form):
        res = super().form_valid(form)
        if res.status_code == 200:
            user = get_user_model().objects.filter(email=form.cleaned_data['email'])
            if user and not user.first().is_verified:
                user = user.first()
                kwargs = {'link': 'http://localhost%s' % reverse('myauth:verify', kwargs={'uuid': user.uuid}),
                          'user': user.username}
                sendler_mail.delay('', '', settings.DEFAULT_FROM_EMAIL, [user.email],
                                   template_name='back_task/mail_registr.html', **kwargs)
        return res
