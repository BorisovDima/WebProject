from django.shortcuts import render
from django.views.generic import FormView
from .models import Dialog
from django.contrib.auth import get_user_model
from .forms import DialogForm



from django.contrib.auth.mixins import LoginRequiredMixin

class DialogView(LoginRequiredMixin, FormView):
   template_name = 'chat/dialog.html'
   form_class = DialogForm

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       if self.kwargs.get('id_dialog'):
           context['dialog'] = Dialog.objects.get(id=self.kwargs['id_dialog'])
           context['dialog'].auth_user(self.request.user)
       else:
            user = get_user_model().objects.get(username=self.kwargs['username'])
            context['dialog'], context['status'] = Dialog.objects.get_or_create_dialog(self.request.user, user)
       print(context)
       return context


