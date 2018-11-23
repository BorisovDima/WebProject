from django.shortcuts import render
from django.views.generic import CreateView
from .forms import MyRegForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LogoutView, LoginView


class Registr(CreateView):
    template_name = 'account/registration.html'
    form_class = MyRegForm
    model = get_user_model()
    success_url = '/'

    def form_valid(self, form):
        resp = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return resp

class Login(LoginView):
    template_name = 'account/registration.html'


class Logout(LogoutView):
    template_name = 'account/registration.html'
    next_page = '/'