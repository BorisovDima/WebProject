from django.views.generic import DeleteView
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from project.apps.blog.shortcuts import render_to_html

class DeleteObj(LoginRequiredMixin, DeleteView):
    model = None
    template_name = None

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return JsonResponse({'status': 'invalid'})
        obj._delete() if kwargs['action'] == 'delete' else obj._return()
        html = render_to_html(self.template_name, {'event': kwargs['event'], 'id': obj.id, 'objs': (obj,)}, request)
        return JsonResponse({'status': 'ok', 'event': kwargs['event'], 'html': html})

    def get(self, request, *args, **kwargs):
        raise Http404



