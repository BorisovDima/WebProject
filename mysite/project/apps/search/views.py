from django.views.generic import TemplateView
from django.urls import reverse

from project.apps.ajax_utils.mixins import AjaxLoaderMixin
from .mixins import QueryStringMixin
from project.apps.blog.mixins import CacheMixin


class Search(QueryStringMixin, AjaxLoaderMixin, CacheMixin, TemplateView):
    model = None
    template_name = 'search/search.html'
    cache_time = 5

    def get_location(self):
         return reverse('search:search')


