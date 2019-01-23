from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from . import views
from .forms import ProfileForm, ProfileFormHead, ProfileFormPhoto, ChangeEmail

app_name = 'account'

urlpatterns = [

    path('p/<slug:login>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile', 'title_user': True}, name='profile'),

    path('p/<slug:login>/post/<int:init>/', views.ProfileView.as_view(form_class=ProfileForm),
         {'location': 'profile', 'title_user': True}, name='profile-post'),



    path('settings/', TemplateView.as_view(template_name='account/settings.html'),
         {'title': 'Settings'}, name='profile-settings'),

    path('settings/change-pass/', views.MyPasswordChangeView.as_view(success_url='/'), name='change-pass'),

    path('settings/change-email/', views.MyEmailChangeView.as_view(success_url='/',
                                                                   model = get_user_model(),
                                                                   form_class = ChangeEmail
                                                                    ), name='change-email'),

    path('p/<slug:login>/change/head/', views.ProfileView.as_view(form_class=ProfileFormHead),
         {'location': 'profile'}, name='change-head'),

    path('p/<slug:login>/change/image/', views.ProfileView.as_view(form_class=ProfileFormPhoto),
         {'event': 'photo', 'location': 'profile'}, name='change-photo'),

    path('p/<slug:login>/<path:location>/', views.ProfileView.as_view(form_class=ProfileForm),
          {'title_user': True}),



]


