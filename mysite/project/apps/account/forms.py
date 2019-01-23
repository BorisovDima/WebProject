from django.contrib.auth import get_user_model
from django.forms import widgets
from django import forms
from .models import Profile #ProfileImg
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import gettext as _


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
                    'placeholder': _('Your name')})

        self.fields['date_of_birth'].widget = widgets.SelectDateWidget(
            attrs={'Class': ' mx-1 my-1 col-3 border custom-select',
                   'style':  'box-shadow: none;',}, years=list(range(1950, 2018)))

        self.fields['date_of_birth'].label = _('Birthday')



    def clean(self):
        return super().clean()

    class Meta:
        model = Profile
        fields = ['about_me', 'date_of_birth', 'country', 'user_name', 'image', 'head']
        widgets = {'country': CountrySelectWidget(attrs={'class': 'border-0 custom-select shadow-none'})}



from project.apps.blog.utils import make_thumbnail
from django.conf import settings

from os.path import splitext

class BaseUserPhotoForm(forms.ModelForm):

    def check_image(self, image):
        if getattr(image, 'image', None):
            if image.size > (2000 * 1000):
                raise forms.ValidationError(_('Max size file 2mb'))
            file, ext = splitext(image.name.lower())
            if ext not in ('.jpeg', '.jpg', '.png'):
                raise forms.ValidationError(_('Unsupported format'))

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

class ChangeEmail(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_('Requared'))
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('User with this email already exists'))
        return self.cleaned_data['email']


    class Meta:
        model = get_user_model()
        fields = ['email']
