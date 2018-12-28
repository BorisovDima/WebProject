from django.urls import path
from . import views
from .forms import ProfileForm, ProfileFormHead, ProfileFormPhoto, ChangeEmail


app_name = 'account'

urlpatterns = [

    path('profile/<slug:login>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile'}, name='profile'),

    path('profile/<slug:login>/followers/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile'}, name='profile-followers'),
    path('profile/<slug:login>/following/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile'}, name='profile-following'),

    path('profile/<slug:slug>/settings/', views.Settings.as_view(slug_field='username',
                                                                 form_class=ChangeEmail),
                                                                 name='profile-settings'),

    path('profile/settings/change-pass/', views.MyPasswordChangeView.as_view(success_url='/')),

    path('profile/<slug:login>/change-header/', views.ProfileView.as_view(form_class=ProfileFormHead),
         {'location': 'profile'}, name='change-head'),

    path('profile/<slug:login>/change-photo/', views.ProfileView.as_view(form_class=ProfileFormPhoto),
         {'event': 'photo', 'location': 'profile'}, name='change-photo'),


]

