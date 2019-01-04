from django.views.generic import DeleteView
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from project.apps.comments.templatetags.comment_tags import get_context

class DeleteObj(LoginRequiredMixin, DeleteView):
    model = None
    template_name = None

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return JsonResponse({'status': 'invalid'})
        obj._delete() if kwargs['action'] == 'delete' else obj._return()
        if kwargs['action'] == 'return' and kwargs['event'] == 'comment':
            initial = obj.id if not obj.initial_comment else obj.initial_comment.id
            html = render_to_string(self.template_name, get_context(obj, request.user, initial), request)
        else:
            html = render_to_string(self.template_name, {'event': kwargs['event'], 'id': obj.id, 'objs': (obj,)}, request)
        return JsonResponse({'status': 'ok', 'event': kwargs['event'], 'html': html})

    def get(self, request, *args, **kwargs):
        raise Http404