from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<slug:username>/dialog/', views.DialogView.as_view(), name='dialog'),
    path('dialog/<int:id_dialog>/', views.DialogView.as_view(), name='old-dialog'),
    path('list-dialogs/<slug:username>/', views.ListDialogView.as_view(), name='list-dialog'),
]
