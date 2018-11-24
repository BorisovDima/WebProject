from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import widgets
from django import forms
class MyRegForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Login'})

        self.fields['username'].help_text += ' And length login minimum  characters'

        self.fields['username'].label = 'Login'
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Password'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                   'placeholder': 'Password'})

    def clean_username(self):
        if len(self.cleaned_data['username']) < 5:
            raise forms.ValidationError('Too short!')
        return self.cleaned_data['username']

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields =['username']

class MyLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Login'})
        self.fields['password'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                       'placeholder': 'Password'})
