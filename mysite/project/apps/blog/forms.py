from django.forms import ModelForm, widgets, ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

from .models import Article

from os.path import splitext
import logging

logger = logging.getLogger(__name__)

class BaseCreateForm(ModelForm):

    def clean_image(self):
        if getattr(self.cleaned_data['image'], 'image', None):
            if self.cleaned_data['image'].size > (1000 * 1000):
                raise ValidationError(_('You can upload an image in JPG, GIF or PNG formats. Max size file 1mb'))
            file, ext = splitext(self.cleaned_data['image'].name.lower())
            if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
                raise ValidationError('Неподдерживаемый формат')

        return self.cleaned_data['image']


class CreatePostForm(BaseCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 6, 'style':
                                                              'resize:none; font-size: 14px',
                                                              'maxlength': settings.MAX_POST_SIZE,
                                                              'id': 'navbar-create_post_form'})

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('image') and not cleaned_data.get('text'):
            raise ValidationError('((Nothing))')
        return cleaned_data

    class Meta:
        model = Article
        fields = ['text', 'image']



class UpdatePostForm(CreatePostForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'style':
                                                              'box-shadow: none; resize:none; font-size: 14px',
                                                              'maxlength': settings.MAX_POST_SIZE,
                                                              'id': 'update-post-text',
                                                               'rows': ''})

    def clean(self):
        cleaned_data = super().clean()
        expired = self.instance.create_data + timezone.timedelta(hours=24)
        if timezone.now() > expired:
            logger.error('Change error: Date %s, Now %s' % (expired, timezone.now()))
            raise ValidationError('Time expired')
        return cleaned_data
