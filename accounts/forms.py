from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomCreationForm(UserCreationForm):
    name = forms.CharField(help_text=None)
    username = forms.CharField(help_text=None)
    email = forms.EmailField(help_text=None)
    password1 = forms.CharField(help_text=None, widget=forms.PasswordInput)
    password2 = forms.CharField(help_text=None, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name','username', 'email', 'password1', 'password2']



class UserForm(forms.ModelForm):
    username = forms.CharField(help_text=None)

    class Meta:
        model = User
        fields = ['name','username', 'email', 'avatar', 'bio']


