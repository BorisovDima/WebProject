from django.forms import ModelForm, widgets, ValidationError
from .models import Article
from .utils import replacer
from PIL import Image
from os.path import splitext
MAX_LENGTH_POST = 484




class BaseCreateForm(ModelForm):

    def clean_text(self):
        self.cleaned_data['text'] = replacer(self.cleaned_data['text'], 44)
        return self.cleaned_data['text']

    def clean_image(self):
        if self.cleaned_data['image']:
            if self.cleaned_data['image'].size > (1000 * 1000):
                raise ValidationError('Very big size photo')
            file, ext = splitext(self.cleaned_data['image'].name.lower())
            if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
                raise ValidationError('Not support format')
        return self.cleaned_data['image']


class CreateArticleForm(BaseCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 6, 'style':
                                                              'resize:none; font-size: 14px',
                                                              'placeholder': 'Title'})

        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 11, 'style':
                                                              'resize:none; font-size: 14px',
                                                               'placeholder': 'Body'})

        self.fields['thread'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
        self.fields['tags'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
        self.fields['thread'].empty_label = 'Choice category...'


    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title) < 50:
            raise ValidationError('Not Title')
        title = replacer(title, 44)
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or len(text) < 100:
            raise ValidationError('Not Text')
        return super().clean_text()


    class Meta:
        model = Article
        fields = ['title', 'text', 'thread', 'tags', 'image', 'status']




class CreatePostForm(BaseCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 6, 'style':
                                                              'resize:none; font-size: 14px',
                                                               'maxlength': MAX_LENGTH_POST})

    def clean_text(self):

        if len(self.cleaned_data['text']) > MAX_LENGTH_POST:
            raise ValidationError('Very big size')
        return super().clean_text()


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('image') and not cleaned_data.get('text'):
            raise ValidationError('Nothing')
        return cleaned_data


    class Meta:
        model = Article
        fields = ['text', 'thread', 'tags', 'image', 'status']



