from django.views.generic import DetailView
from django.http import JsonResponse
from django.template.loader import render_to_string




class GetChild(DetailView):

    def get(self, req, *args, **kwargs):
        comment_parent = self.get_object()
        initial = comment_parent.id
        comments = comment_parent.initial_comment_set.all().reverse()
        return JsonResponse({'html': render_to_string(self.template_name, {'comments': comments,
                                                                           'initial': initial},
                                                                                         req)})




