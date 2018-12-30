from django.shortcuts import render
from django.views.generic import TemplateView

class Search(TemplateView):
    model = None
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context