from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import widgets
from django import forms
from .models import Profile #ProfileImg

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

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about_me'].widget = widgets.Textarea(attrs={'Class': 'form-control', 'rows': 2,
                                                                 'style':'resize:none; font-size: 14px'})

    def clean_user_img(self):
        if getattr(self.cleaned_data['user_img'], 'image', None):
            if self.cleaned_data['user_img'].size > (1000 * 1000):
                raise forms.ValidationError('Very big size photo')

            if self.cleaned_data['user_img'].image.height < 250 or \
                    self.cleaned_data['user_img'].image.width < 250:
                raise forms.ValidationError('Very big size photo')
        return self.cleaned_data['user_img']

    def clean_about_me(self):
        return self.cleaned_data['about_me']

    class Meta:
        model = Profile
        fields = ['about_me', 'date_of_birth', 'current_city', 'user_img']