from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def RegistrantLoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_registrant:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")

                return redirect(f'/registrant/{user.registrant.pk}')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "loginRegistrant.html",
                    context={"form":form})

def LGULoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_lgu:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")

                return redirect(f'/lgu/{user.lgu.pk}')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "loginLGU.html",
                    context={"form":form})


def LogoutRequest(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

from lgu.models import LocalGovernmentUnit


def LandingPage(request):
    lgus = LocalGovernmentUnit.objects.values_list('name', flat=True)
    return render(
        request=request,
        template_name="landingPage.html",
        context={
            'lgus': lgus,
        }
    )