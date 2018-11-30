from django.views.generic import DetailView
from django.views.generic import FormView
from .models import Dialog
from django.contrib.auth import get_user_model
from .forms import DialogForm
from django.http import Http404


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





class ListDialogView(LoginRequiredMixin, DetailView):
    template_name = 'chat/list_dialog.html'
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        if self.request.user != self.object:
            raise Http404
        context = super().get_context_data(**kwargs)
        context['dialogs'] = self.object.profile.get_user_dialogs()
        context['list_dialogs'] = self.request.path
        return context


