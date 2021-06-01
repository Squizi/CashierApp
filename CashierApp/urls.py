from django.urls import path
from .views import RegistrationView, SignInView, ResidentsView, AddPaymentsView, SingleResidentView, PersonDetailsView
from . import views

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('signup/', views.signup, name='signup'),
    path('payment/', AddPaymentsView.as_view(), name='payment'),
    path('signin/', views.signin, name='signin'),
    path('index/', views.index,  name='index'),
    path('', views.index, name='index'),
    path('signout/', views.signout, name='signout'),
    path('resident/', SingleResidentView.as_view(), name='resident'),
    path('addresident/', views.addresident, name='addresident'),
    path('addpayment/', views.addpayment, name='addpayment'),
    path('persondetails/<int:id>/', views.persondetails,  name='persondetails'),
    path('pay/<int:id>/', views.pay,  name='pay'),
]
