from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from .utils import delete_cache
from hashlib import md5

class CacheMixin:
     cache_time = 10

     def get_uniq_key(self, req):
        key = repr(req) + req.user.username or 'anon-user'
        hash_ = md5(key.encode())
        return hash_.hexdigest()

     def get(self, request, *args, **kwargs):
        uniq_key = self.get_uniq_key(request)
        response = cache.get(uniq_key)
        print(response)
        if not response:
            response = super().get(request, *args, **kwargs)
            response = response.render() if hasattr(response, 'render') else response
            cache.add(uniq_key, response, self.cache_time * 60)
        return response

     def delete_cache(self, *args):
        key = make_template_fragment_key(*args)
        delete_cache(key)