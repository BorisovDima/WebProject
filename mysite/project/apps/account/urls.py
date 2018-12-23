from django.urls import path
from . import views
from .forms import ProfileForm, ProfileFormHead, ProfileFormPhoto
from django.views.generic import TemplateView


app_name = 'account'

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('verify/', TemplateView.as_view(template_name='account/verify.html'), name='verify_page'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),

    path('profile/<slug:login>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile'}, name='profile'),

    path('profile/<slug:login>/change-header/', views.ProfileView.as_view(form_class=ProfileFormHead),
         {'location': 'profile', 'ajax': True}, name='change-head'),

    path('profile/<slug:login>/change-photo/', views.ProfileView.as_view(form_class=ProfileFormPhoto),
         {'event': 'photo', 'ajax': True}, name='change-photo'),

]

