from django import forms
from .models import PostComment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'mdl-textfield__input'}))

    class Meta:
        model = PostComment
        fields = ['comment']
