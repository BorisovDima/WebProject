from django.http import JsonResponse
from django.views.generic import View, DetailView
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count
from project.apps.blog.models import Community
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from project.apps.like_dislike.models import Subscribe

class Loader_sorted(View):
    template_name = None # Указывается в urls.py
    model = None         # Указывается в urls.py
    sorted_kwargs = {}
    paginate = 10

    def get(self, req, **kwargs):
        self.since = req.GET.get('since')
        params = {self.sorted_kwargs.get('field'): self.kwargs.get('key')} \
            if self.sorted_kwargs.get('field') else {}
        params.update({'is_active': True})
        objs, since = self.get_objs(params, req)
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_string(self.template_name, {'objs': objs}, self.request),
                             'since': since,
                             'status': 'ok'})

    def return_objs(self, objects, field, since_):
        if self.since: objects = objects.filter(**{since_: self.since})
        objs = list(objects[:self.paginate])
        since = getattr(objs[-1], field) if objs else None
        return objs, since


class All(Loader_sorted):
    def get_objs(self, params, req):
        objects = self.model.objects.filter(**params)
        return self.return_objs(objects, 'id', 'id__lt')

class Hot(Loader_sorted):
    def get_objs(self, params, req):
        count = self.sorted_kwargs.get('count') if not self.kwargs.get('key') else Community.objects.get(
            name=self.kwargs['key']).get_hot() * settings.HOT_POST
        objects = self.model.objects.filter(**params)
        objects = objects.annotate(sort=Count('views')).filter(sort__gte=count)
        return self.return_objs(objects, 'id', 'id__lt')

class Top(Loader_sorted):
    def get_objs(self, params, req):
        objects = self.model.objects.filter(**params).annotate(v=Count('views')).order_by('-v')
        return self.return_objs(objects, 'v', 'v__lt')

class Search(Loader_sorted):
    def get_objs(self, params, req):
        objs = self.model.objects.filter(**{self.sorted_kwargs['field']: self.request.GET.get('search')})
        if self.sorted_kwargs.get('option') == 'new':
            return self.return_objs(objs, 'id', 'id__lt')
        return self.return_objs(objs.annotate(count=
                                              Count(self.sorted_kwargs['top_field'])).
                                              order_by('-count'),
                                             'count', 'count__lt')

class Home(Loader_sorted):
    def get_objs(self, params, req):
        subs = Subscribe.objects.filter(user=req.user)
        objects = self.model.objects.filter(author__id__in=subs.filter(type='U').values('object_id'))
        return self.return_objs(objects, 'id', 'id__lt')



##############################################################


class Loader_dialogs(LoginRequiredMixin, Loader_sorted):

    def send_data(self, objs, req):
        since = req.GET.get('since')
        if since:
            objs = objs.filter(id__lt=since)
        button = objs.count() > self.paginate
        objs = list(objs[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_string(self.template_name, {'objs': objs}, req),
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

class Loader_comments(Loader_dialogs):
    def get(self, req, **kwargs):
        objs = self.model.objects.filter(article_id=kwargs['key'], initial_comment=None)
        return self.send_data(objs, req)