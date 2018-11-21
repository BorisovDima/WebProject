from django.shortcuts import render
from django.views.generic import FormView
from .forms import CommentForm
from .models import Comment
from project.apps.blog.models import Article
from project.apps.account.models import BlogUser

class AddComment(FormView):
    form_class = CommentForm

    def form_valid(self, form):
        user = BlogUser.objects.get()
        article = Article.objects.get(slug=self.kwargs['slug'])
        text = form.cleaned_data['text']
        Comment.objects.create(author=user, article=article, text=text)

        return super().form_valid(form)

