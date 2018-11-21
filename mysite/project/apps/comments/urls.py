from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('<categories:category>/<slug:slug>/add-comment/', views.AddComment.as_view(), name='add_comment'),
]
