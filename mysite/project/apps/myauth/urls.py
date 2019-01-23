from django.urls import path
from . import views
from .forms import MyPasswordResetForm, MySetPasswordForm,  MyLoginForm, ActivEmail, MyRegForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import get_user_model

app_name = 'myauth'

urlpatterns = [

    path('login/', views.Login.as_view(template_name = 'myauth/registration.html',
                                       form_class = MyLoginForm),
                                        {'title': 'Login'},
                                        name='login'),

    path('registration/', views.Registr.as_view(template_name = 'myauth/registration.html',
                                        form_class = MyRegForm,
                                        model=get_user_model(),
                                        success_url='/'),
                                        {'title': 'Registration'},
                                        name='registration'),

    path('login/password-reset/', views.ResetPass.as_view(success_url = '/login/',
                                        email_template_name='back_task/reset_mail.html',
                                        html_email_template_name='back_task/reset_mail.html',
                                        form_class=MyPasswordResetForm)),

    path('login/help/', views.HelpLogin.as_view(template_name = 'myauth/help.html',
                                        form_class = ActivEmail,
                                        success_url='/login/help/'),
                                        {'title': 'Help'},
                                        name='login-help'),

    path('login/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                                        template_name = 'myauth/reset_pass_form.html',
                                        success_url='/login/',
                                        form_class=MySetPasswordForm),
                                        name='password_reset_confirm'),

    path('logout/', views.Logout.as_view(template_name = 'myauth/registration.html',
                                        next_page = '/'),
                                        name='logout'),
    path('verify/<uuid:uuid>/', views.Vertify_account.as_view(), name='verify'),



]