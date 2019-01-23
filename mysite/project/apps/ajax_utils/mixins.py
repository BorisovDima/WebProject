from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Count


from project.apps.like_dislike.models import Subscribe
from  .models import AjaxLoaderModel

HOT_POST = 2

class Sort:

    def return_objs(self, objects, field, since_):
        if self.since: objects = objects.filter(**{since_: self.since})
        objs = list(objects[:self.location.paginate])
        since = getattr(objs[-1], field) if objs else None
        return objs, since

    def All(self, req, objs):
        return self.return_objs(objs, 'id', 'id__lt')

    def Hot(self, req, objs):
        objects = objs.annotate(sort=Count(self.location.top_field)).filter(sort__gte=HOT_POST)
        return self.return_objs(objects, 'id', 'id__lt')

    def Top(self, req, objs):
        objects = objs.annotate(count=Count(self.location.top_field)).order_by('-count')
        return self.return_objs(objects, 'count', 'count__lt')

    def Home(self, req, objs):
        subs = Subscribe.objects.filter(user=req.user)
        objects = objs.filter(author_id__in=subs.filter(type='U').values('object_id'))
        return self.return_objs(objects, 'id', 'id__lt')


class AjaxLoaderMixin(Sort):
    model = AjaxLoaderModel

    def get_data(self, req):
        method = self.get_sort_method()
        objs = self.get_objs(req)
        return method(req, objs)

    def get_objs(self, req):
        return self.model.objects.loader(req, self.location)

    def get_sort_method(self):
        try:
            return getattr(self, self.location.sort)
        except Exception as i:
            print(i)
            raise Http404


    def dispatch(self, req, *args, **kwargs):
        location = kwargs['location']
        self.location = get_object_or_404(AjaxLoaderModel, location=location)
        self.since = req.GET.get('since')
        return super().dispatch(req, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'], context['type'] = self.location.location, self.location.type
        context['start_location'] = self.get_location()[1:-1]
        if self.location.detail:
            context['id_location'] = self.object.id
        return context
