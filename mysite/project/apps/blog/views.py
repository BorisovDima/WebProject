from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST


from project.apps.ajax_utils_.mixins import AjaxMixin
from project.apps.ajax_utils.mixins import AjaxLoaderMixin
from project.apps.account.utils import get_user_recommends
from project.apps.account.mixins import OnlyOwnerMixin
from .mixins import CacheMixin



class MainPage(AjaxLoaderMixin, CacheMixin, TemplateView):
    cache_time = 5

    def get_location(self):
        return reverse('blog:main_page')


class DetailArticle(AjaxMixin,  DetailView):

    def post(self, req, **kwargs):
        post = self.get_object()
        if req.user.is_authenticated:
            post.viewed(req.user)
        return self.get_json(req, extra={'url': post.get_absolute_url()}, objs=(post,))


@method_decorator(require_POST, name='dispatch')
class CreateArticle(LoginRequiredMixin, AjaxMixin, CreateView):

    def post(self, req, *args, **kwargs):
        self.path = req.POST.get('path')
        return super().post(req, *args, **kwargs)

    def get_data(self, form):
        context = {'html': render_to_string('blog/publish.html'), 'add': False}
        user_home = reverse('account:profile', kwargs={'login': self.request.user.username})
        if user_home == self.path:
            context.update({'post': render_to_string('blog/articles.html',
                                                     {'objs': (self.object,)},
                                                     self.request),
                                                     'add': True})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response


class UpdateArticle(OnlyOwnerMixin, AjaxMixin, CacheMixin, UpdateView):

    def get_data(self, form):
        return {'html': render_to_string('blog/articles.html', {'objs': (self.object,)}, self.request)}

    def get(self, req, *args, **kwargs):
        self.object = self.get_object()
        return self.get_json(req, **self.get_context_data())

    def form_valid(self, form):
        if self.request.POST.get('delete'):
            form.instance.image = None
        self.delete_cache('post', [str(self.object.id)])
        return super().form_valid(form)



class Recommend(AjaxMixin, View):
    template_name = 'tag/home_sidebar.html'

    def get(self, req, **kwargs):
        return self.get_json(req, **get_user_recommends(req.user, req, 30))





