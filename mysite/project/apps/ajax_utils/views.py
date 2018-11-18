from django.shortcuts import render

from django.views.generic import ListView


class Loader(ListView):
    template_name = None
    model = None