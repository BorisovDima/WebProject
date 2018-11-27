from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/<slug:login>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:login>/dialogs/', views.ListDialogView.as_view(), name='dialogs')
]

