from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from .models import BlogUser

import logging

logger = logging.getLogger(__name__)

class NotLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

class OnlyOwnerMixin:
    def dispatch(self, req, *args, **kwargs):
        obj = self.get_object()
        user = obj if isinstance(obj, BlogUser) else obj.get_user
        if user != req.user:
            logger.error('OnlyOwnerMixin: User - %s, Owner - %s' % (req.user.username or '-A', user.username))
            raise HttpResponseForbidden
        return super().dispatch(req, *args, **kwargs)

