from django.urls import path
from . import views
from .models import Profile
from .forms import ProfileForm, ProfileFormHead, ProfileFormPhoto
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('verify/', TemplateView.as_view(template_name='account/verify.html'), name='verify_page'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),

    path('profile/<slug:login>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'user-articles'}, name='profile'),

    path('profile/<slug:login>/change-head/', views.ProfileView.as_view(form_class=ProfileFormHead),
         {'location': 'user-articles'}, name='change-head'),

    path('profile/<slug:login>/change-photo/', views.ProfileView.as_view(form_class=ProfileFormPhoto),
         {'location': 'user-articles'}, name='change-photo'),

]

