from django.urls import path
from .views import RegistrationView, SignInView, ResidentsView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('', ResidentsView.as_view(), name='index'),
]