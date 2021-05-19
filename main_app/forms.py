from django.forms.widgets import TextInput
from django.forms import ModelForm
from .models import Comment, Picture


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = Comment
        fields = ['text']

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['name', 'image']
