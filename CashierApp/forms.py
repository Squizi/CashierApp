from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Cashier


class CreateUserForm(UserCreationForm):
    block = forms.CharField(max_length=255, required=True, help_text='Required. Mas len 255.')

    class Meta:
        model = Cashier
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'block']
