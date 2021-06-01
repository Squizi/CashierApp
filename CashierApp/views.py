from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import Resident, Payment
from CashierApp.forms import CreateUserForm, CreateResidentForm, CreatePaymentForm
import smtplib
import ssl
from email.mime.text import MIMEText as text
import json


# Views

# Class based view.
class RegistrationView(TemplateView):
    template_name = 'registration.html'


class SignInView(TemplateView):
    template_name = 'signin.html'


class ResidentsView(TemplateView):
    template_name = 'index.html'


class SingleResidentView(TemplateView):
    template_name = 'resident.html'


class PersonDetailsView(TemplateView):
    template_name = 'persondetails.html'


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


def persondetails(request, id):
    resident = Resident.objects.get(id=id)
    payments = Payment.objects.filter(resident__id=id)
    context = {'resident': resident, 'payments': payments}
    return render(request, 'persondetails.html', context)


def pay(request, id):
    payment = Payment.objects.get(id=id)
    payment.status = "Paid"
    payment.save()
    resident = payment.resident
    message = f"""You have successfully paid ${payment.amount} for {payment.type}."""

    sendemail(resident.email, message)
    return redirect(f'/persondetails/{resident.id}/')


def sendemail(receiver, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "nefyna.emailservice@gmail.com"  # Sender's email address

    msg = text(message)
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = 'Your Cashier payment'

    with open("./Cashier/credentials.json", "r") as jsonfile:
        data = json.load(jsonfile)
        password = data["password"]

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, msg.as_string())
