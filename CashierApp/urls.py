from django.urls import path
from .views import RegistrationView

urlpatterns = [
    path('', RegistrationView, name='registration')
]