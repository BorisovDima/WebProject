from django.forms import ModelForm, widgets
from .models import Message



class DialogForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = widgets.Textarea(attrs={'Class': 'form-control',
                                                             'rows': 3, 'style':
                                                             'resize:none; font-size: 14px',
                                                             'maxlength': 500,
                                                             'id': 'id_text_dialog'
                                                             })

    class Meta:
        model = Message
        fields = ['text']