from django import forms
from .models import CustomUser
from Post.models import Post


class CustomUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
    date_of_birth = forms.DateField(label='Date Of Birth',
                                    widget=forms.DateInput(attrs={'class': 'mdl-textfield__input'}))

    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_admin', 'last_login']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'mdl-textfield__input'}))

    class Meta:
        model = Post
        exclude = ['created_at', 'user', 'likes', 'liked_at']
