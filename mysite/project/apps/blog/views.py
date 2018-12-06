from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, TemplateView, FormView, ListView
from .models import Article, Thread
from django.shortcuts import get_object_or_404
from .shortcuts import render_to_html
from project.apps.comments.forms import CommentForm
from  .forms import CreateArticleForm, CreatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin



class MainPage(TemplateView):

    def get_context_data(self, **kwargs):
        self.template_name = self.kwargs['template_name']
        return super().get_context_data(**kwargs)


class DetailArticle(DetailView):
    model = Article
    template_name = 'blog/DetailArticle.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user.is_authenticated:
            obj.viewed(user)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm()
        return context



class CreateArticle(LoginRequiredMixin, CreateView):
    template_name = 'blog/CreateArticle.html'
    model = None
    form_class = None
    status = None
    not_success = None


    def form_valid(self, form):
        if self.model == Article:
            form.instance.author = self.request.user
            form.instance.status = self.status
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(self.not_success) if self.not_success else super().form_invalid(form)


class ThreadsView(TemplateView):
    context_object = None
    template_name = None

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['objs'] = self.context_object if not self.kwargs.get('thread') \
            else Thread.objects.get(name=self.kwargs.get('thread'))
        return cont
