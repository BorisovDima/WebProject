from django.views.generic import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.db.models import Q

class Autocomplete(View):
    model = None
    max_length = None

    def get(self, req, *args, **kwargs):
        q = req.GET['value']
        qs = self.model.objects.all()
        if q:
            qs = qs.filter(Q(username__istartswith=q) | Q(profile__user_name__istartswith=q)).annotate(subs=Count('my_followers')).order_by('subs')
        list = [{'value': render_to_string('autocomplete/authocomplit-icon.html', {'obj': i}), 'login': i.username}
                for i in qs[:self.max_length]]
        return JsonResponse({'list': list})
