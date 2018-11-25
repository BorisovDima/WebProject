from django.shortcuts import render
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from .models import Article, Category
from django.shortcuts import get_object_or_404
from .shortcuts import render_to_html
from project.apps.comments.forms import CommentForm
from  .forms import CreateArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin



class MainPage(TemplateView):

    def get_context_data(self, **kwargs):
        self.template_name = self.kwargs['template_name']
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



class CreateArticle(LoginRequiredMixin, CreateView):
    template_name = 'blog/CreateArticle.html'
    model = Article
    form_class = CreateArticleForm
    #success_url  - automat

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




