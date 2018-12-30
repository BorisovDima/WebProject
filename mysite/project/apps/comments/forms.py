from django.forms import ModelForm
from django import forms
from .models import Comment




class CommentForm(ModelForm):
    parent = forms.IntegerField(required=False, widget=forms.widgets.HiddenInput)


    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'Class': 'form-control',
                                          'maxlength': 424,
                                          'style': 'resize:none; font-size: 14px',
                                          'data-type': 'data-form',
                                          'placeholder': 'Оставить комментарий'
                                          })
        }


