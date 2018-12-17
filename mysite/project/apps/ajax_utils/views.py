from django.http import JsonResponse
from django.views.generic import View, DetailView
from project.apps.blog.shortcuts import render_to_html
from django.conf import settings
from django.db.models import Count
from project.apps.blog.models import Thread
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

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
        objects = self.model.objects.filter(**{self.sorted_kwargs.get('field'): req.GET.get('search')}, active=True)
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
        objects = self.model.objects.filter(**params, active=True).exclude(rating=0).order_by('rating')
        if self.since: objects = objects.filter(rating__gt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].rating if objs else None
        return objs, since

    def hot(self, params, count):
        objects = self.model.objects.filter(**params, active=True)
        objects = objects.annotate(sort=Count('views')).filter(sort__gte=count)
        if self.since: objects = objects.filter(id__lt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].id if objs else None
        return objs, since


    def all(self, params):
        objects = self.model.objects.filter(**params, active=True)
        if self.since: objects = objects.filter(id__lt=self.since)
        objs = list(objects[:self.paginate])
        since = objs[-1].id if objs else None
        return objs, since

from django.db.models import Q
from project.apps.like_dislike.models import Subscribe
from project.apps.blog.models import Thread
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

class Loader_home(Loader_search):
    def get(self, req, **kwargs):
        since = req.GET.get('since')
        subs = Subscribe.objects.filter(user=req.user)
        thread = ContentType.objects.get_for_model(Thread)
        user = ContentType.objects.get_for_model(get_user_model())
        objects = self.model.objects.filter(Q(author__id__in=subs.filter(content_type=user).values('object_id'))
                                           |Q(thread__id__in=subs.filter(content_type=thread).values('object_id'))
                                            , active = True)

        if since:
            objects = objects.filter(id__lt=since)
        objs = list(objects[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})

class Loader_dialogs(LoginRequiredMixin, Loader_search):

    def send_data(self, objs, req):
        since = req.GET.get('since')
        if since:
            objs = objs.filter(id__lt=since)
        button = objs.count() > self.paginate
        objs = list(objs[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, req),
                             'since': objs[-1].id,
                             'status': 'ok',
                             'button': button})

    def get(self, req, **kwargs):
        objs = req.user.profile.get_user_dialogs()
        return self.send_data(objs, req)


class Loader_notify(Loader_dialogs):
    def get(self, req, **kwargs):
        objs = self.model.objects.filter(owner=req.user)
        return self.send_data(objs, req)

