from project.apps.account.mixins import AjaxMixin, NotLoginRequiredMixin
from project.apps.account.models import Profile
from .models import BanList
from django.http import Http404
from django.urls import reverse
from .utils import handler_ip
from django.template.loader import render_to_string
from django.views.generic import CreateView, RedirectView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from .forms import MyPasswordResetForm, MySetPasswordForm, MyRegForm, MyLoginForm, ActivEmail



class Registr(NotLoginRequiredMixin, AjaxMixin, CreateView):
    template_name = 'myauth/registration.html'
    form_class = MyRegForm
    model = get_user_model()
    success_url = '/'
    captcha = True

    def get(self, req, *args, **kwargs): raise Http404

    def get_data(self, form):
        return {'html': render_to_string('myauth/verify.html', {'user': form.instance.username,
                                                                            'mail': form.instance.email})}


class Login(NotLoginRequiredMixin, LoginView):
    template_name = 'myauth/registration.html'
    form_class = MyLoginForm

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



class Logout(LogoutView):
    template_name = 'myauth/registration.html'
    next_page = '/'


class Vertify_account(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        model = get_user_model()
        try:
            user = model.objects.get(uuid=self.kwargs['uuid'], is_verified=False)
        except model.DoesNotExist:
            raise Http404
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        Profile.objects.create(name=user.username, bloguser=user)
        self.url = reverse('myauth:login')
        return super().get_redirect_url(*args, **kwargs)


from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


class ResetPass(AjaxMixin, PasswordResetView):
    success_url = '/login/'
    email_template_name = 'back_task/reset_mail.html'
    html_email_template_name = 'back_task/reset_mail.html'
    form_class = MyPasswordResetForm


    def get(self, req, *args, **kwargs): raise Http404

    def get_data(self, form):
        return {'html': render_to_string('myauth/reset_pass.html', {'email': form.cleaned_data['email']})}


class ResetPassConfirm(PasswordResetConfirmView):
    template_name = 'myauth/reset_pass_form.html'
    success_url = '/login/'
    form_class = MySetPasswordForm

from django.views.generic import FormView
from project.apps.back_task.tasks import send_verify

class HelpLogin(NotLoginRequiredMixin, AjaxMixin, FormView):
    template_name = 'myauth/help.html'
    form_class = ActivEmail
    captcha = True
    success_url = '/login/help/'

    def get_data(self, form):
        return {'email': form.cleaned_data['email']}

    def form_valid(self, form):
        res = super().form_valid(form)
        if res.status_code == 200:
            user = get_user_model().objects.filter(email=form.cleaned_data['email'])
            if user and not user.first().is_verified:
                user = user.first()
                send_verify.delay(user.uuid, user.email, user.username)
        return res
