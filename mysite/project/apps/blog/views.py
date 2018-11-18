from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
PAGINATE = 10



class MainPage(ListView):
    template_name = 'blog/MainPage'
    model = Article


class DetailArticle(DetailView):
    pass