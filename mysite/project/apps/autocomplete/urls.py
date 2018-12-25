from django.urls import path
from . import views
from django.contrib.auth import get_user_model

MAX_OBJECTS = 10

urlpatterns = [
    path('autocomplete/', views.Autocomplete.as_view(model=get_user_model(), max_length=MAX_OBJECTS),
         name='autocomplete'),

]