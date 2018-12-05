from django.http import JsonResponse
from django.views.generic import View
from project.apps.blog.shortcuts import render_to_html


def get_sort_params():
    pass


class Loader(View):
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
        if req.GET.get('search'):
            params = {self.sorted_kwargs.get('field'): req.GET.get('search')}
            objects = self.model.objects.filter(**params)
            print(objects)
        elif self.sorted_kwargs:
            params = {self.sorted_kwargs.get('field'): self.kwargs.get('key')}
            objects = self.model.objects.filter(**params)
        else:
            objects = self.model.objects.all()
        if since:
            objects = objects.filter(id__lte=(int(since)-1))
        objs = list(objects[:self.paginate])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})


