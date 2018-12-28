from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from .models import Profile
from django.http import Http404
from .mixins import AjaxMixin



class MyPasswordChangeView(AjaxMixin, PasswordChangeView):
    def get(self, req, *args, **kwargs):
        raise Http404

    def get_data(self, form):
        return {'text': 'Password change!', 'type': 'password'}



class Settings(AjaxMixin, UpdateView):
    template_name = 'account/settings.html'
    model = get_user_model()
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != kwargs['slug']:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_data(self, form):
        return {'text': 'Email change!', 'type': 'email'}



class ProfileView(AjaxMixin, UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    slug_field = 'name'
    slug_url_kwarg = 'login'
    form_class = None

    def get_data(self, form):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['user_status'] = 'anonim'
        else:
            context['user_status'] = 'owner' \
                if self.kwargs['login'] == self.request.user.profile.name else 'user'
        context['start_location'] = self.kwargs['location'] + '/' + self.kwargs['login']
        context['location'] = self.request.path[1:-1]
        return context

    def post(self, req, *args, **kwargs):
        profile = self.get_object()
        if profile.bloguser != req.user:
            raise Http404
        return super().post(req, *args, **kwargs)