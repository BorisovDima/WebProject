from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, TemplateView
from .models import Article, Community
from project.apps.account.mixins import AjaxMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class MainPage(LoginRequiredMixin, TemplateView):


    def get_context_data(self, **kwargs):
        print(self.request.user.id)
        self.template_name = self.kwargs['template_name']
        context = super().get_context_data(**kwargs)
        return context


class CreateArticle(LoginRequiredMixin, AjaxMixin, CreateView):
    template_name = None
    model = None
    form_class = None
    success_url = '/'

    def get(self, *args, **kwargs):
        raise Http404

    def get_data(self, form):
        return {'html': render_to_string('blog/publish.html')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


from django.http import JsonResponse
class ViewPost(DetailView):
    model = Article

    def post(self, req, *args, **kwargs):
        post = self.get_object()
        post.viewed(req.user)
        return JsonResponse({})




class CommunityView(TemplateView):
    template_name = None

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        if self.kwargs.get('community'):
            cont['objs'] = Community.objects.get(name=self.kwargs.get('community'))
            cont['location'] = cont['location'].replace('sort', self.kwargs['community'])
        cont['search_loc'] = self.kwargs.get('search')
        return cont



