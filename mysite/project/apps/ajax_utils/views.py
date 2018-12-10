from django.http import JsonResponse
from django.views.generic import View
from project.apps.blog.shortcuts import render_to_html
from django.conf import settings
from django.db.models import Count
from project.apps.blog.models import Thread

class Loader_search(View):
    template_name = None # Указывается в urls.py
    model = None         # Указывается в urls.py
    sorted_kwargs = {}
    paginate = 10
    """
    Получаю обьект по которому производить сортировку и id с которого отбирать множество (rows.id < since). 
    Обертываю QuerySet в list и у последего обьекта беру id с которого при следующем запросе брать множество, 
    если пустой QuerySet, то возвращаю json со стасуом != "ok". Html рендю в обычный текст.
    """

    def get(self, req, **kwargs):
        since = req.GET.get('since')
        objects = self.model.objects.filter(**{self.sorted_kwargs.get('field'): req.GET.get('search')})
        if since:
            objects = objects.filter(id__lt=int(since))
        objs = list(objects[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})


class Loader_sorted(Loader_search):

    def get(self, req, **kwargs):
        self.since = req.GET.get('since')
        sort = self.sorted_kwargs.get('sorted')
        params = {self.sorted_kwargs.get('field'): self.kwargs.get('key')} \
            if self.sorted_kwargs.get('field') else {}
        if sort == 'top': objs, since = self.top(params)
        elif sort == 'hot':
            count = 0 if not params else Thread.objects.get(name=self.kwargs['key']).get_hot() * settings.HOT_POST
            objs, since = self.hot(params, count)
        else: objs, since = self.all(params)
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': since,
                             'status': 'ok'})

    def top(self, params):
        objects = self.model.objects.filter(**params).exclude(rating=0).order_by('-rating')
        if self.since: objects = objects.filter(rating__lt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].rating if objs else None
        return objs, since

    def hot(self, params, count):
        objects = self.model.objects.filter(**params)
        objects = objects.annotate(sort=Count('views')).filter(sort__gte=count)
        if self.since: objects = objects.filter(id__lt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].id if objs else None
        return objs, since


    def all(self, params):
        objects = self.model.objects.filter(**params)
        if self.since: objects = objects.filter(id__lt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].id if objs else None
        return objs, since

from django.db.models import Q

class Loader_home(Loader_search):

    def get(self, req, **kwargs):
        print(self.model.objects.filter(thread__in=req.user.thread_set.all()))
        since = req.GET.get('since')
        objects = self.model.objects.filter(Q(thread__in=req.user.thread_set.all()) |
                                            Q(author__in=req.user.bloguser_set.all()))
        print(objects, req.user.bloguser_set.all(), req.user.thread_set.all())
        if since:
            objects = objects.filter(rating__lt=since)
        objs = list(objects[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})
