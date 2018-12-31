from django.forms import ModelForm, widgets, ValidationError
from .models import Article, Community
from .utils import replacer
from PIL import Image
from os.path import splitext

MAX_LENGTH_POST = 484

MAX_LENGTH_SUB_COMMUNITY = 124
MAX_LENGTH_NAME_COMMUNITY = 50

MIN_LENGTH_SUB_COMMUNITY = 17
MIN_LENGTH_NAME_COMMUNITY = 3

class BaseCreateForm(ModelForm):

    def clean_text(self):
        self.cleaned_data['text'] = replacer(self.cleaned_data['text'], 44)
        return self.cleaned_data['text']

    def clean_image(self):
        if getattr(self.cleaned_data['image'], 'image', None):
            if self.cleaned_data['image'].size > (1000 * 1000):
                raise ValidationError('Максимальный размер файла 1mb')
            file, ext = splitext(self.cleaned_data['image'].name.lower())
            if ext not in ('.jpeg', '.jpg', '.png', '.gif'):
                raise ValidationError('Неподдерживаемый формат')

        return self.cleaned_data['image']


#class CreateArticleForm(BaseCreateForm):
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['title'].widget = widgets.Textarea(attrs={'Class': 'form-control',
#                                                              'rows': 6, 'style':
#                                                              'resize:none; font-size: 14px',
#                                                              'placeholder': 'Title'})
#
#        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
#                                                              'rows': 11, 'style':
#                                                              'resize:none; font-size: 14px',
#                                                               'placeholder': 'Body'})
#
#        self.fields['community'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
 #       self.fields['tags'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
 #       self.fields['community'].empty_label = 'Choice category...'
#
#
#    def clean_title(self):
#        title = self.cleaned_data.get('title')
#        if not title or len(title) < 50:
#            raise ValidationError('Not Title')
#        title = replacer(title, 44)
#        return title
#
#    def clean_text(self):
#        text = self.cleaned_data.get('text')
#        if not text or len(text) < 100:
#            raise ValidationError('Not Text')
#        return super().clean_text()
#
#
#    class Meta:
 #       model = Article
#        fields = ['title', 'text', 'community', 'tags', 'image', 'status']




class CreatePostForm(BaseCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 6, 'style':
                                                              'resize:none; font-size: 14px',
                                                              'maxlength': MAX_LENGTH_POST,
                                                              'id': 'navbar-create_post_form'})

        self.fields['community'].widget.attrs.update({'style': 'display:none'})

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
        fields = ['text', 'community', 'tags', 'image', 'status']





class CreateCommunityForm(BaseCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['sub'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                              'rows': 3, 'style':
                                                              'resize:none; font-size: 14px',
                                                              'maxlength':MAX_LENGTH_SUB_COMMUNITY,
                                                              'id': 'create_community_sub_form'})
        self.fields['sub'].help_text = 'Description: max lenght-' + str(MAX_LENGTH_SUB_COMMUNITY)

        self.fields['name'].widget = widgets.TextInput(attrs={'Class': 'form-control',
                                                            'style': 'resize:none; font-size: 14px',
                                                            'maxlength': MAX_LENGTH_NAME_COMMUNITY,
                                                            'id': 'create_community_name_form'})
        self.fields['name'].help_text = 'Name community: format <name> or <name>_<name>'
        self.fields['image'].help_text = 'Choice image: max size 1mb'


    def clean_name(self):

        if len(self.cleaned_data['name']) > MAX_LENGTH_NAME_COMMUNITY:
            raise ValidationError('Max length ' + str(MAX_LENGTH_NAME_COMMUNITY))

        if len(self.cleaned_data['name']) < MIN_LENGTH_NAME_COMMUNITY:
            raise ValidationError('Min length ' + str(MIN_LENGTH_NAME_COMMUNITY))

        if replacer(self.cleaned_data['name'], 20, bool_=True):
            raise ValidationError('Not valid')

        if ' ' in self.cleaned_data['name']:
            raise ValidationError('Space character, use only _')

        return self.cleaned_data['name']


    def clean_sub(self):

        if len(self.cleaned_data['sub']) > MAX_LENGTH_SUB_COMMUNITY:
            raise ValidationError('Max length ' + str(MAX_LENGTH_SUB_COMMUNITY))

        if len(self.cleaned_data['sub']) < MIN_LENGTH_SUB_COMMUNITY:
            raise ValidationError('Min length ' + str(MIN_LENGTH_SUB_COMMUNITY))

        if replacer(self.cleaned_data['sub'], 30, bool_=True):
            raise ValidationError('Not valid')

        return self.cleaned_data['sub']


    class Meta:
        model = Community
        fields = ['name', 'sub', 'image']
