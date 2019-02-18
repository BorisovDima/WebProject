from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Dialog
from .forms import DialogForm

import logging

logger = logging.getLogger()

class DialogView(LoginRequiredMixin, FormView):
   template_name = 'chat/dialog.html'
   form_class = DialogForm

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       if self.kwargs.get('id_dialog'):
           context['dialog'] = Dialog.objects.get(id=self.kwargs['id_dialog'])
           if context['dialog'].auth_user(self.request.user):
               logger.error('Dialog %d not auth %s' % (self.kwargs['id_dialog'], self.request.user))
               raise Http404
       else:
            user = get_user_model().objects.get(username=self.kwargs['username'])
            context['dialog'], context['status'] = Dialog.objects.get_or_create_dialog(self.request.user, user)
       return context



