from django.urls import path
from . import views
from blog.models import Article
from comments.models import Comment

app_name = 'ajax_utils'

urlpatterns = [
    path('api/load/', views.Loader.as_view(model=Article,
                                           template_name='ajax_utils/articles.html'), name='art_loader'),

]