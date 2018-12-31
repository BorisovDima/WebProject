from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, TemplateView
from .models import Article
from project.apps.account.mixins import AjaxMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse


class MainPage(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        self.template_name = self.kwargs['template_name']
        context = super().get_context_data(**kwargs)
        return context


class CreateArticle(LoginRequiredMixin, AjaxMixin, CreateView):
    template_name = None
    model = None
    form_class = None
    success_url = '/'

    def post(self, req, *args, **kwargs):
        self.path = req.POST.get('path')
        return super().post(req, *args, **kwargs)

    def get(self, *args, **kwargs):
        raise Http404

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
        form.instance.set_tags()
        return response


from django.http import JsonResponse
class ViewPost(DetailView):
    model = Article

    def post(self, req, *args, **kwargs):
        post = self.get_object()
        post.viewed(req.user)
        return JsonResponse({})





#class CommunityView(TemplateView):
   # template_name = None

   # def get_context_data(self, **kwargs):
   #     cont = super().get_context_data(**kwargs)
   #     if self.kwargs.get('community'):
   #        cont['objs'] = Community.objects.get(name=self.kwargs.get('community'))
    #        cont['location'] = cont['location'].replace('sort', self.kwargs['community'])
   #     cont['search_loc'] = self.kwargs.get('search')
    #    return cont



