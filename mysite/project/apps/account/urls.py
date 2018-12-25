from django.urls import path, include
from . import views
from .forms import ProfileForm, ProfileFormHead, ProfileFormPhoto
from django.views.generic import TemplateView


app_name = 'account'

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('login/password-reset/', views.ResetPass.as_view()),
    path('login/help/', views.HelpLogin.as_view(), name='login-help'),

    path('login/reset/<uidb64>/<token>/', views.ResetPassConfirm.as_view(), name='password_reset_confirm'),

    path('logout/', views.Logout.as_view(), name='logout'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),

    path('profile/<slug:login>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile'}, name='profile'),

    path('profile/<slug:login>/change-header/', views.ProfileView.as_view(form_class=ProfileFormHead),
         {'location': 'profile'}, name='change-head'),

    path('profile/<slug:login>/change-photo/', views.ProfileView.as_view(form_class=ProfileFormPhoto),
         {'event': 'photo'}, name='change-photo'),


]

