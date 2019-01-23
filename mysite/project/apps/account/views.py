from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .mixins import OnlyOwnerMixin
from project.apps.ajax_utils_.mixins import AjaxMixin
from project.apps.ajax_utils.mixins import AjaxLoaderMixin


@method_decorator(require_POST, name='dispatch')
class MyPasswordChangeView(LoginRequiredMixin, AjaxMixin, PasswordChangeView):

    def get_data(self, form):
        return {'text': _('Password change!'), 'type': 'password'}


@method_decorator(require_POST, name='dispatch')
class MyEmailChangeView(LoginRequiredMixin, AjaxMixin, UpdateView):

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)

    def get_data(self, form):
        return {'text': _('Email change!'), 'type': 'email'}



class ProfileView(OnlyOwnerMixin, AjaxLoaderMixin, AjaxMixin, UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    slug_field = 'name'
    slug_url_kwarg = 'login'
    form_class = None

    def get_data(self, form):
        return {}

    def get_location(self):
        return reverse('account:profile', kwargs={'login': self.kwargs['login']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_status'] = 'owner' if self.kwargs['login'] == self.request.user.username else 'user'
        context['init'] = self.kwargs.get('init')
        return context
