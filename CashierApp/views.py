from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.


class RegistrationView(TemplateView):
    template_name = 'registration.html'

class SignInView(TemplateView):
    template_name = 'signin.html'

class ResidentsView(TemplateView):
    template_name = 'index.html'