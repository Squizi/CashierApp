from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import Resident, Payment
from CashierApp.forms import CreateUserForm, CreateResidentForm, CreatePaymentForm


# Create your views here.


class RegistrationView(TemplateView):
    template_name = 'registration.html'


class SignInView(TemplateView):
    template_name = 'signin.html'


class ResidentsView(TemplateView):
    template_name = 'index.html'


class SingleResidentView(TemplateView):
    template_name = 'resident.html'


def index(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    residents = Resident.objects.filter(cashier=request.user)
    context = {'residents': residents}
    return render(request, 'index.html', context)


class AddPaymentsView(TemplateView):
    template_name = 'payment.html'


def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CreateUserForm()
    return render(request, 'registration.html', {'form': form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="signin.html", context={"login_form": form})


def signout(request):
    logout(request)
    messages.info(request, "You have successfully signed out.")
    return redirect("signin")


def addresident(request):
    if request.method == 'POST':
        form = CreateResidentForm(request.POST)

        form.cashier = request.user

        if form.is_valid():
            resident = Resident()
            resident.full_name = form["full_name"].value()
            resident.email = form["email"].value()
            resident.apartment = form["apartment"].value()
            resident.cashier = request.user
            resident.save()
            return redirect('index')
    else:
        form = CreateResidentForm()
    return render(request, 'resident.html', {'form': form})


def addpayment(request):
    if request.method == 'POST':
        form = CreatePaymentForm(request.POST)

        residents = Resident.objects.filter(cashier=request.user)

        for r in residents:
            p = Payment()
            p.type = form["type"].value()
            p.status = form["status"].value()
            p.amount = form["amount"].value()
            p.date = form["date"].value()
            p.resident = r
            p.save()
        return redirect('index')
    else:
        form = CreatePaymentForm()
    return render(request, 'payment.html', {'form': form})
