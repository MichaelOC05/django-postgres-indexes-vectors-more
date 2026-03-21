from django import forms
from django.contrib.auth.forms import UserCreationForm

from forkprojectapplication.accounts.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
