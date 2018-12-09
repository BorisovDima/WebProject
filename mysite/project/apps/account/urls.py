from django.urls import path
from . import views
from .models import Profile #ProfileImg
from .forms import ProfileForm #ProfileImgForm
from django.views.generic import TemplateView

app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('verify/', TemplateView.as_view(template_name='account/verify.html'), name='verify_page'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),
    path('profile/<slug:login>/subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path('profile/<slug:login>/', views.ProfileView.as_view(), {'location': 'user-articles'}, name='profile'),


]

