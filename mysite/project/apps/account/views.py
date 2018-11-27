from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import MyRegForm, MyLoginForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from .models import Profile
from .forms import ProfileForm

class Registr(CreateView):
    template_name = 'account/registration.html'
    form_class = MyRegForm
    model = get_user_model()
    success_url = '/'

    def form_valid(self, form):
        form.instance.profile = Profile.objects.create(login=form.cleaned_data['username'])
        resp = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return resp

class Login(LoginView):
    template_name = 'account/registration.html'
    form_class = MyLoginForm


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
            print(context)
        return context

class ListDialogView(DetailView):
    template_name = 'account/list_dialog.html'
    model = Profile
    slug_field = 'login'
    slug_url_kwarg = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dialogs'] = self.object.get_user_dialogs()
        return context