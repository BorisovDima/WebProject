from django.urls import path
from django.views.generic import TemplateView
from . import views, forms

app_name = 'info'

urlpatterns = [
    path('load_template/<path:url>/', views.Info.as_view()),
    path('send/message/', views.QuestionView.as_view(template_name='info/site_form.html',
                                                     form_class=forms.QuestionForm),
                                                    {'type': 'msg'}, name='send-message'),
    path('send/email/', views.QuestionView.as_view(template_name='info/email_form.html',
                                                   form_class=forms.QuestionFormEmail),
                                                    {'type': 'email'}, name='send-email'),

    path('<path:url>/', views.Info.as_view(template_name='info/info-main.html'), {'title': 'info'}, name="dispatch"),

]
