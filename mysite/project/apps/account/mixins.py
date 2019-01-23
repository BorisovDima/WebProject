from django.shortcuts import redirect
from django.http import Http404

from .models import BlogUser


class NotLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class OnlyOwnerMixin:
    def post(self, req, *args, **kwargs):
        obj = self.get_object()
        user = obj if isinstance(obj, BlogUser) else obj.get_user
        if user != req.user:
            raise Http404
        return super().post(req, *args, **kwargs)

