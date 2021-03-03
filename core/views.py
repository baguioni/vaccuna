from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lgu.models import LocalGovernmentUnit
from registrant.models import Individual


def LandingPage(request):
    lgus = LocalGovernmentUnit.objects.all()
    return render(
        request=request,
        template_name="landingPage.html",
        context={'lgus': lgus}
    )


def RegistrantLoginView(request):
    form = AuthenticationForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_registrant:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect(f'/registrant/{user.registrant.pk}')
        else:
            error = "User does not exist."
            messages.error(request, "User does not exist.")
            context['error'] = error
            return render(request = request,
                template_name = "loginRegistrant.html",
                context=context)

    return render(request = request,
                    template_name = "loginRegistrant.html",
                    context=context)

def LGULoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_lgu:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")

            return redirect(f'/lgu/{user.lgu.pk}')
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


@api_view(['GET'])
def QRCodeRead(request, pk):
    response = {}
    if request.method == 'GET':
        individual = Individual.objects.get(pk=pk)
        date1 = individual.first_vaccination_datetime.date()
        date2 = individual.second_vaccination_datetime.date()
        today = date.today()
        if date1 == today or date2 == today and individual.vaccination_status != 2:
            individual.vaccination_status += 1
        return redirect(f'/vaccination/status/{individual.pk}')


def UpdateVaccinationStatus(request, pk):
    individual = Individual.objects.get(pk=pk)
    date1 = individual.first_vaccination_datetime
    date2 = individual.second_vaccination_datetime
    date = date1 if date1 else date2 if date2 else 'None'
    message_success = 'Successfull updated vaccination status!'
    message_fail = f'Invalid. Scan QR Code on your scheduled date.'
    context = {
        'message': message_success if individual.vaccination_status != 0 else message_fail,
        'name': individual.get_full_name,
        'date': date,
        'status': individual.vaccination_status,
    }

    return render(
        request=request,
        template_name='vaccinationStatus.html',
        context=context,
    )
