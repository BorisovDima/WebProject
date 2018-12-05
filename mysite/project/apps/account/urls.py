from django.urls import path
from . import views
from .models import Profile #ProfileImg
from .forms import ProfileForm #ProfileImgForm
app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/<slug:login>/subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path('profile/<slug:login>/', views.ProfileView.as_view(), {'location': 'user-articles'}, name='profile'),

]

