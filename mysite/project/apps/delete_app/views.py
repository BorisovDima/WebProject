from django.views.generic import DeleteView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from project.apps.ajax_utils_.mixins import AjaxMixin
from project.apps.comments.templatetags.comment_tags import get_context


@method_decorator(require_POST, name='dispatch')
class DeleteObj(LoginRequiredMixin, AjaxMixin, DeleteView):
    model = None
    template_name = None

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return JsonResponse({'status': 'invalid'})
        obj._delete() if kwargs['action'] == 'delete' else obj._return()
        if kwargs['action'] == 'return' and kwargs['event'] == 'comment':
            initial = obj.id if not obj.initial_comment else obj.initial_comment.id
            context = get_context(obj, request.user, initial)
        else:
            context = {'id': obj.id, 'objs': (obj,), 'event': kwargs['event']}
        return self.get_json(request, **context, extra={'status': 'ok', 'event': kwargs['event']})
