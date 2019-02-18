from django.views.generic import DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from project.apps.ajax_utils_.mixins import AjaxMixin
from project.apps.comments.templatetags.comment_tags import get_context
from project.apps.account.mixins import OnlyOwnerMixin

import logging

logger = logging.getLogger(__name__)

@method_decorator(require_POST, name='dispatch')
class DeleteObj(OnlyOwnerMixin, AjaxMixin, DeleteView):
    model = None
    template_name = None

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj._delete() if kwargs['action'] == 'delete' else obj._return()
        if kwargs['action'] == 'return' and kwargs['event'] == 'comment':
            initial = obj.id if not obj.initial_comment else obj.initial_comment.id
            context = get_context(obj, request.user, initial)
        else:
            context = {'id': obj.id, 'objs': (obj,), 'event': kwargs['event']}
        return self.get_json(request, **context, extra={'status': 'ok', 'event': kwargs['event']})
