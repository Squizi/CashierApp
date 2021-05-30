from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from CashierApp.forms import CreateUserForm



# Create your views here.


class RegistrationView(TemplateView):
    template_name = 'registration.html'


class SignInView(TemplateView):
    template_name = 'signin.html'


class ResidentsView(TemplateView):
    template_name = 'index.html'


def index(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    return render(request, 'index.html')


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