from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import widgets
from django import forms
from .models import Profile #ProfileImg

class MyRegForm(UserCreationForm):

    email = forms.EmailField(required=True, widget=
                    forms.widgets.EmailInput(attrs={'Class': 'form-control'}))

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


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('requared')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exist')
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
                                                                  'placeholder': 'Login'})
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
            raise forms.ValidationError('User not verified, please check email', code='not verify', params={'id': id})

        return self.cleaned_data['username']

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about_me'].widget = widgets.Textarea(attrs={'Class': 'form-control', 'rows': 2,
                                                                 'style':'resize:none; font-size: 14px',
                                                                 'maxlength': 120})

        self.fields['about_me'].label = 'About me'

        self.fields['user_name'].widget = widgets.TextInput(
            attrs={'Class': 'text-dark col-6 my-1 py-0 border-0 ',
                   'style':'font-size: 24px; box-shadow: none;',
                    'placeholder':'Your name'})

        self.fields['date_of_birth'].widget = widgets.SelectDateWidget(
            attrs={'Class': ' mx-1 my-1 col-3 border custom-select',
                   'style':  'box-shadow: none;',}, years=list(range(1950, 2018)))

        self.fields['date_of_birth'].label = 'Date of birthday'

        self.fields['current_city'].widget = widgets.TextInput(
            attrs={'Class': 'col-6 my-1 border-0',
                  'style':'font-size: 14px; box-shadow: none;',
                   'placeholder':'Your location'})
    def clean(self):
        return super().clean()

    class Meta:
        model = Profile
        fields = ['about_me', 'date_of_birth', 'current_city', 'user_name', 'image', 'head']



from project.apps.blog.utils import make_thumbnail
from django.conf import settings

from os.path import splitext

class BaseUserPhotoForm(forms.ModelForm):

    def check_image(self, image):
        print(getattr(image, 'image', None), '----')
        if getattr(image, 'image', None):
            if image.size > (1000 * 1000):
                raise forms.ValidationError('Максимальный размер файла 1mb')
            file, ext = splitext(image.name.lower())
            if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
                raise forms.ValidationError('Неподдерживаемый формат')

class ProfileFormPhoto(BaseUserPhotoForm):

    def clean_image(self):
        self.check_image(self.cleaned_data['image'])
        return self.cleaned_data['image']

    def save(self, commit=True):
        make_thumbnail(self.instance.image, (settings.MAX_WIDTH_IMG, settings.MAX_HEIGHT_IMG),
                       icon=(settings.USER_ICON, self.instance.thumbnail))
        return super().save(commit)

    class Meta:
        model = Profile
        fields = ['image']


class ProfileFormHead(BaseUserPhotoForm):

    def clean_head(self):
        self.check_image(self.cleaned_data['head'])
        return self.cleaned_data['head']

    def save(self, commit=True):
        make_thumbnail(self.instance.head, (settings.MAX_WIDTH_HEAD, settings.MAX_HEIGHT_HEAD))
        return super().save(commit)

    class Meta:
        model = Profile
        fields = ['head']