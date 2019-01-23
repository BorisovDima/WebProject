from django.views.generic import DetailView
from django.http import JsonResponse
from project.apps.ajax_utils_.mixins import AjaxMixin




class GetChild(AjaxMixin, DetailView):

    def get(self, req, *args, **kwargs):
        comment_parent = self.get_object()
        initial = comment_parent.id
        comments = comment_parent.initial_comment_set.all().reverse()
        return self.get_json(req, **{'comments': comments,'initial': initial})




