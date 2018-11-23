from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class MyRegForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

