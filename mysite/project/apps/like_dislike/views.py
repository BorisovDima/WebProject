from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LikeSubscribe(LoginRequiredMixin, View):
    model = None
    foreign_model = None
    type = None
    event = None

    def post(self, req, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs['id'])
        try:
            inst = self.foreign_model.objects.get(type=self.type,
                                           user=req.user, object_id=obj.id)
            inst.delete()
            add = False
        except self.foreign_model.DoesNotExist:
            if self.event == 'like':
                obj.like.create(user=req.user, type=self.type)
            else:
                obj.my_followers.create(user=req.user, type=self.type)
            add = True
        count = obj.like.all() if self.event == 'like' else obj.my_followers.all()
        return JsonResponse({'count': count.count(),'add': add})
