from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView, View, RedirectView
from .forms import MyRegForm, MyLoginForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from .models import Profile
from .forms import ProfileForm #ProfileImgForm
from django.http import Http404
from django.urls import reverse


class Registr(CreateView):
    template_name = 'account/registration.html'
    form_class = MyRegForm
    model = get_user_model()
    success_url = '/verify/'

    def form_valid(self, form):
        form.instance.profile = Profile.objects.create(login=form.cleaned_data['username'])
        resp = super().form_valid(form)
        return resp

class Login(LoginView):
    template_name = 'account/registration.html'
    form_class = MyLoginForm

    def form_invalid(self, form):
        print(form.errors.as_json())
        return super().form_invalid(form)

class Logout(LogoutView):
    template_name = 'account/registration.html'
    next_page = '/'


class ProfileView(UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    slug_field = 'login'
    slug_url_kwarg = 'login'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['user_status'] = 'anonim'
        else:
            context['user_status'] = 'owner' \
                if self.kwargs['login'] == self.request.user.profile.login else 'user'
        context['location'] = self.kwargs['location'] + '/' + self.kwargs['login']
        return context


class Vertify_account(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        model = get_user_model()
        try:
            user = model.objects.get(uuid=self.kwargs['uuid'], is_verified=False)
        except model.DoesNotExist:
            raise Http404
        user.is_verified = True
        user.save()
        self.url = reverse('account:login')
        return super().get_redirect_url(*args, **kwargs)

