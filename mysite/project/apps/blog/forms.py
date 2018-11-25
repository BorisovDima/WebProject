from django.forms import ModelForm, widgets
from .models import Article
from .utils import replacer
class CreateArticleForm(ModelForm):

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

        self.fields['category'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
        self.fields['tags'].widget.attrs.update({'Class': 'custom-select my-1 mr-sm-2'})
        self.fields['category'].empty_label = 'Choice category...'


    def clean_title(self):
        self.cleaned_data['title'] = replacer(self.cleaned_data['title'], 44)
        return self.cleaned_data['title']

    def clean_text(self):
        self.cleaned_data['text'] = replacer(self.cleaned_data['text'], 44)
        return self.cleaned_data['text']

    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'tags']

