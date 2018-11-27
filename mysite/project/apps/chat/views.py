from django.shortcuts import render
from django.views.generic import FormView
from .models import Dialog
from django.contrib.auth import get_user_model
from .forms import DialogForm
from django.db.models import Count


from django.contrib.auth.mixins import LoginRequiredMixin

class DialogView(LoginRequiredMixin, FormView):
   template_name = 'chat/dialog.html'
   form_class = DialogForm

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       if self.kwargs.get('id_dialog'):
           context['dialog'] = Dialog.objects.get(id=self.kwargs['id_dialog'])
       else:
            user = get_user_model().objects.get(username=self.kwargs['username'])
            dialog = Dialog.objects.filter(to_user=user, from_user=self.request.user) or \
                    Dialog.objects.filter(from_user=user, to_user=self.request.user)
            print(dialog)
            print(self.request.user, user)
            if not dialog:
                context['dialog'] = Dialog.objects.create(from_user=self.request.user, to_user=user)
                context['status'] = 'New'
            else:
                context['dialog'] = dialog.get()
       print(context['dialog'], '22222222222222222222222222222222222222222222')
       return context





