from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<slug:username>/dialog/', views.DialogView.as_view(), kwargs={'title': 'Dialog'}, name='dialog'),
    path('dialog/<int:id_dialog>/', views.DialogView.as_view(), kwargs={'title': 'Dialog'}, name='old-dialog'),
]
