from django.views.generic import DeleteView, DetailView
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

class DeleteObj(LoginRequiredMixin, DeleteView):
    model = None
    template_name = None

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.author:
            return JsonResponse({'status': 'invalid'})
        obj._delete() if kwargs['action'] == 'delete' else obj._return()
        html = render_to_string(self.template_name, {'event': kwargs['event'], 'id': obj.id, 'objs': (obj,)}, request)
        return JsonResponse({'status': 'ok', 'event': kwargs['event'], 'html': html})

    def get(self, request, *args, **kwargs):
        raise Http404


class GetChild(DetailView):

    def get(self, req, *args, **kwargs):
        comment_parent = self.get_object()
        initial = comment_parent.id
        comments = comment_parent.initial_comment_set.all().reverse()
        return JsonResponse({'html': render_to_string(self.template_name, {'comments': comments,
                                                                           'initial': initial},
                                                                                         req)})




