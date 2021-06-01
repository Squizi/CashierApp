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

# Class based view for registration.
class RegistrationView(TemplateView):
    template_name = 'registration.html'


# Class based view for sign in.
class SignInView(TemplateView):
    template_name = 'signin.html'


# Class based view for index page.
class ResidentsView(TemplateView):
    template_name = 'index.html'


# Class based view for resident page.
class SingleResidentView(TemplateView):
    template_name = 'resident.html'


# Class based view for person details page.
class PersonDetailsView(TemplateView):
    template_name = 'persondetails.html'


# View for index
def index(request):
    # Checks if the user is logged in and if not it redirects it to the Sign In page
    if not request.user.is_authenticated:
        return redirect("signin")

    # takes all residents that are connected to the logged user
    residents = Resident.objects.filter(cashier=request.user)
    context = {'residents': residents}
    return render(request, 'index.html', context)


# Class based view for payment page.
class AddPaymentsView(TemplateView):
    template_name = 'payment.html'


# Function for registration
def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            form.save()  # saves everything to database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CreateUserForm()
    return render(request, 'registration.html', {'form': form})


# Sign In function
def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        # Check if form is valid
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


# Sign Out function
def signout(request):
    logout(request)
    messages.info(request, "You have successfully signed out.")
    return redirect("signin")


# Function that adds new resident for the logged in cashier
def addresident(request):
    # Checks if the user is logged in and if not it redirects it to the Sign In page
    if not request.user.is_authenticated:
        return redirect("signin")

    if request.method == 'POST':
        form = CreateResidentForm(request.POST)

        form.cashier = request.user

        # Check if form is valid
        if form.is_valid():
            # Create new resident
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


# Function that adds new payment for the residents of the logged in cashier
def addpayment(request):
    # Checks if the user is logged in and if not it redirects it to the Sign In page
    if not request.user.is_authenticated:
        return redirect("signin")

    if request.method == 'POST':
        form = CreatePaymentForm(request.POST)

        residents = Resident.objects.filter(cashier=request.user)

        # for every resident we add a new payment
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


# Function that gives information for the requested resident
def persondetails(request, id):
    # Checks if the user is logged in and if not it redirects it to the Sign In page
    if not request.user.is_authenticated:
        return redirect("signin")

    resident = Resident.objects.get(id=id)  # get the resident that is wanted from the database
    payments = Payment.objects.filter(resident__id=id)  # get the payments that are connected to the resident
    context = {'resident': resident, 'payments': payments}
    return render(request, 'persondetails.html', context)


# Function to change payment status from Unpaid to Paid for the requested resident
def pay(request, id):
    # Checks if the user is logged in and if not it redirects it to the Sign In page
    if not request.user.is_authenticated:
        return redirect("signin")

    # Changes the status of the payment to paid and saves it in the database.
    payment = Payment.objects.get(id=id)
    payment.status = "Paid"
    payment.save()

    resident = payment.resident
    # Create message to send to the resident that have paid.
    message = f"""You have successfully paid ${payment.amount} for {payment.type}."""

    # Call function sendemail()
    sendemail(resident.email, message)
    return redirect(f'/persondetails/{resident.id}/')


# Function that sends emails
def sendemail(receiver, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "nefyna.emailservice@gmail.com"  # Sender's email address

    # Creating how the email would look like when it is sent
    msg = text(message)
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = 'Your Cashier payment'

    # Read file to see the password of the sender's email
    with open("./Cashier/credentials.json", "r") as jsonfile:
        data = json.load(jsonfile)
        password = data["password"]

    # Sends email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, msg.as_string())
