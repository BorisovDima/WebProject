from django.urls import path
from . import views


app_name = 'myauth'

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Registr.as_view(), name='registration'),
    path('login/password-reset/', views.ResetPass.as_view()),
    path('login/help/', views.HelpLogin.as_view(), name='login-help'),

    path('login/reset/<uidb64>/<token>/', views.ResetPassConfirm.as_view(), name='password_reset_confirm'),

    path('logout/', views.Logout.as_view(), name='logout'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),

]