from django.http import JsonResponse
from django.views.generic import View
from project.apps.blog.shortcuts import render_to_html


class Loader(View):
    template_name = None # Указывается в urls.py
    model = None         # Указывается в urls.py

    """
    Получаю обьект по которому производить сортировку и id с которого отбирать множество (rows.id < since). 
    Обертываю QuerySet в list и у последего обьекта беру id с которого при следующем запросе брать множество, 
    если пустой QuerySet, то возвращаю json со стасуом != "ok". Html рендю в обычный текст.
    """

    def get(self, req, **kwargs):
        obj_loader, since = req.GET.get('obj_id'), req.GET.get('since')
        objects = self.model.objects.filter(category__name=obj_loader.strip()) if obj_loader \
            else self.model.objects.all() #Сортирую по имени моей категории ForeignKey или отдаю все посты
        if since:
            objects = objects.filter(id__lte=(int(since)-1))
        objs = list(objects[:15])
        if not objs: return JsonResponse({'status': 'end'})
        return JsonResponse({'html': render_to_html(self.template_name, {'objs': objs}, self.request),
                             'since': objs[-1].id,
                             'status': 'ok'})


