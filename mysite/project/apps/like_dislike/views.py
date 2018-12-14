from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
import json
from django.http import JsonResponse


class LikeSubscribe(LoginRequiredMixin, View):
    model = None
    foreign_model = None
    type = None

    def post(self, req, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs['id'])
        try:
            inst = self.foreign_model.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                           user=req.user, object_id=obj.id)
            inst.delete()
            add = False
        except self.foreign_model.DoesNotExist:
            if self.type == 'like':
                obj.like.create(user=req.user)
            else:
                obj.my_followers.create(user=req.user)
            add = True
        count = obj.like.all() if self.type == 'like' else obj.my_followers.all()
        return JsonResponse({'count': count.count(),'add': add})
