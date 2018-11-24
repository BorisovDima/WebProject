from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Article, Category
from django.shortcuts import get_object_or_404
from .shortcuts import render_to_html
from project.apps.comments.forms import CommentForm



class MainPage(TemplateView):
    template_name = 'blog/MainPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class DetailArticle(DetailView):
    model = Article
    template_name = 'blog/DetailArticle.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.viewed()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm()
        return context

#class CreatePost()