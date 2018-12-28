from django.http import JsonResponse
from django.views.generic import View, DetailView
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count
from project.apps.blog.models import Community
from django.contrib.auth.mixins import LoginRequiredMixin


class Loader_sorted(View):
    template_name = None # Указывается в urls.py
    model = None         # Указывается в urls.py
    sorted_kwargs = {}
    paginate = 10

    def get(self, req, **kwargs):
        self.since = req.GET.get('since')
        sort = self.sorted_kwargs.get('sorted')
        params = {self.sorted_kwargs.get('field'): self.kwargs.get('key')} \
            if self.sorted_kwargs.get('field') else {}
        params.update({'is_active': True})
        if sort == 'top': objs, since = self.top(params)
        elif sort == 'hot':
            count = self.sorted_kwargs.get('count') if not self.kwargs.get('key') else Community.objects.get(name=self.kwargs['key']).get_hot() * settings.HOT_POST
            objs, since = self.hot(params, count)
        elif sort == 'search': objs, since = self.search()
        else: objs, since = self.all(params)
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_string(self.template_name, {'objs': objs}, self.request),
                             'since': since,
                             'status': 'ok'})

    def return_objs(self, objects, field, since_):
        if self.since: objects = objects.filter(**{since_: self.since})
        objs = list(objects[:self.paginate])
        since = getattr(objs[-1], field) if objs else None
        return objs, since

    def search(self):
        objs = self.model.objects.filter(**{self.sorted_kwargs['field']: self.request.GET.get('search')})
        if self.sorted_kwargs.get('option') == 'new':
            return self.return_objs(objs, 'id', 'id__lt')
        return self.return_objs(objs.annotate(count=Count('my_followers')).order_by('-count'),
                                                                        'count', 'count__lt')

    def top(self, params):
        objects = self.model.objects.filter(**params).exclude(rating=0).order_by('rating')
        return self.return_objs(objects, 'rating', 'rating__gt')

    def hot(self, params, count):
        objects = self.model.objects.filter(**params)
        objects = objects.annotate(sort=Count('views')).filter(sort__gte=count)
        return self.return_objs(objects, 'id', 'id__lt')

    def all(self, params):
        objects = self.model.objects.filter(**params)
        return self.return_objs(objects, 'id', 'id__lt')






from django.db.models import Q
from project.apps.like_dislike.models import Subscribe
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

class Loader_home(Loader_sorted):
    def get(self, req, **kwargs):
        since = req.GET.get('since')
        subs = Subscribe.objects.filter(user=req.user)
        community = ContentType.objects.get_for_model(Community)
        user = ContentType.objects.get_for_model(get_user_model())
        objects = self.model.objects.filter(Q(author__id__in=subs.filter(content_type=user).values('object_id'))
                                           |Q(community__id__in=subs.filter(content_type=community).values('object_id'))
                                            ,is_active = True)

        if since:
            objects = objects.filter(id__lt=since)
        objs = list(objects[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_string(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})

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