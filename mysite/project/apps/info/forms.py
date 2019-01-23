from django import forms
from .models import Question
from django.utils.translation import gettext as _

class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.widgets.Textarea(attrs={'Class': 'form-control',
                                                                    'rows': 2,
                                                                    'data-type': 'info-form',
                                                                    'style': 'max-height: 200px',
                                                                    'placeholder': _('Subject matter'),
                                                                    'maxlength': 100})
        self.fields['body'].widget = forms.widgets.Textarea(attrs={'Class': 'form-control',
                                                                   'rows': 4,
                                                                   'data-type': 'info-form',
                                                                   'style': 'max-height: 300px',
                                                                   'placeholder': _('Detail of inquiry'),
                                                                   'maxlength': 400})


    def clean_title(self):
        if len(self.cleaned_data['title']) < 40:
            raise forms.ValidationError(_('Question title very short!. Minimum 40 characters'))
        return self.cleaned_data['title']

    def clean_body(self):
        if len(self.cleaned_data['body']) < 60:
            raise forms.ValidationError(_('Question body very short!. Minimum 60 characters'))
        return self.cleaned_data['body']


    class Meta:
        model = Question
        fields = ['title', 'body']


class QuestionFormEmail(QuestionForm):

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'Class': 'form-control',
                                              'placeholder': 'Email',
                                              })


