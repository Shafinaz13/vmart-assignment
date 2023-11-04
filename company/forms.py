from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['position', 'phone_number']
