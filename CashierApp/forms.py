from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Cashier, Resident, Payment


# Form which inherits the default class UserCreationForm
class CreateUserForm(UserCreationForm):
    block = forms.CharField(max_length=255, required=True, help_text='Required. Has len 255.')

    class Meta:
        model = Cashier
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'block']


# Form which inherits the Model class Residents
class CreateResidentForm(forms.ModelForm):

    class Meta:
        model = Resident
        fields = ['full_name', 'email', 'apartment']


# Form which inherits the Model class Payments
class CreatePaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['type', 'status', 'amount', 'date', 'resident']
