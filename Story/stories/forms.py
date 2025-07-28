from django import forms
from .models import Story, Comment

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['content'].required = False
        self.fields['image'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'