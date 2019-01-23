from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from project.apps.back_task.tasks import sendler_mail
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import widgets
from django import forms
from django.utils.translation import gettext as _

class MyRegForm(UserCreationForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'Class': 'form-control',
                                                    'placeholder': 'Email',
                                                    })

        self.fields['username'].widget = widgets.TextInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Login'})

        self.fields['username'].help_text += ' And length login minimum  characters'

        self.fields['username'].label = 'Login'
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Password'})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                   'placeholder': 'Password agan'})



    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields =['username', 'email']

    def clean_username(self):
        if len(self.cleaned_data['username']) < 3:
            raise forms.ValidationError(_('Too short!. 3 characters minimum'))
        return self.cleaned_data['username']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_('Requared'))
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('User with this email already exists'))
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user


class MyLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'Class': 'form-control',
                                                                  'placeholder': 'Login',
                                                                  'id': 'login_username'})
        self.fields['password'].widget = widgets.PasswordInput(attrs={'Class': 'form-control',
                                                                       'placeholder': 'Password'})

    def clean_username(self):
        model = get_user_model()
        try:
            user = model.objects.get(username=self.cleaned_data.get('username'))
        except model.DoesNotExist:
            raise self.get_invalid_login_error()
        if not user.is_verified:
            id = user.id
            raise forms.ValidationError(_('User not verified,'
                                        ' please check email'), code='not verify', params={'id': id})
        if not user.is_active:
            raise forms.ValidationError(_('User was deleted'))
        return self.cleaned_data['username']





class MyPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = 'Reset mail'
        print(context)
        context.update(user='')
        sendler_mail.delay(subject, body, from_email, [to_email], template_name=html_email_template_name, **context)

class MySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'Class': 'form-control col-6',
                                                     'placeholder': 'Password',
                                                     })
        self.fields['new_password2'].widget.attrs.update({'Class': 'form-control col-6',
                                                     'placeholder': 'Password again',
                                                     })
class ActivEmail(forms.Form):

    email = forms.EmailField(required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'Class': 'form-control',
                                                    'placeholder': 'Email',
                                                    })