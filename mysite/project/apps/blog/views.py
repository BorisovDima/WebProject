from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Article, Category
from django.shortcuts import get_object_or_404
from .shortcuts import render_to_html


PAGINATE = 10



class MainPage(TemplateView):
    template_name = 'blog/MainPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class DetailArticle(DetailView):
    pass