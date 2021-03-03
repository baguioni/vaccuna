from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import UserSignupForm
from registrant.forms import (AddressFieldForm, IndividualFormset,
                              IndividualRegistrantForm)
from registrant.models import Individual, Registrant
import googlemaps
from django.conf import settings
from registrant.tasks import AssignPriorityGroup, DetermineVaccinationSite
from core.tasks import GetCoordinates
import re
from lgu.models import LocalGovernmentUnit

from django.shortcuts import render
from wsgiref.util import FileWrapper
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from lgu.tasks import ScheduleAppointment

def DownloadQRCode(request, id):
    img = Individual.objects.get(pk=id).qr_code
    filename = os.path.basename(img.file.name)
    response = HttpResponse(img.file, content_type='image/jpeg')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def RegistrantDashboard(request, id):
    registrant = Registrant.objects.get(pk=id)
    template = "home.html"
    print(request.user.id, registrant.user.id)
    if request.user.id != registrant.user.id:
        template = "allow.html"
    individuals = registrant.individuals.all()
    base_url = settings.BASE_URL
    context = {
        'registrant': registrant,
        'individuals': individuals,
        'base_url': base_url,
    }
    return render(request, template, context)

def HouseholdRegisterView(request):
    if request.method == "GET":
        address_form = AddressFieldForm(request.GET or None)
        formset = IndividualFormset(queryset=Individual.objects.none())

    if request.method == "POST":
        address_form = AddressFieldForm(request.POST or None)
        formset = IndividualFormset(request.POST)

        if formset.is_valid() and address_form.is_valid():
            address = address_form.save()
            coordinates = GetCoordinates(address)

            if coordinates:
                coordinates = coordinates[0]['geometry']['location']
                address.latitude = coordinates['lat']
                address.longitude = coordinates['lng']

            address.save()

            lgu_name = re.sub("[\(\[].*?[\)\]]", "", address.city).strip()

            lgu = LocalGovernmentUnit.objects.filter(name__contains=lgu_name)
            lgu = lgu[0] if lgu else None
            # Create registrant object
            registrant = Registrant(user=request.user, address=address, is_household=True, lgu=lgu)
            registrant.save()
            vaccination_site = DetermineVaccinationSite(registrant.id)

            for individual_form in formset:
                if individual_form.is_valid():
                    try:
                        individual = individual_form.save(commit=False)
                        individual.registrant = registrant
                        individual.generateQR()
                        individual.lgu = lgu
                        individual.vaccination_site = vaccination_site
                        individual.save()
                        AssignPriorityGroup(individual)

                    except:
                        print('database error')

            if vaccination_site:
                ScheduleAppointment(vaccination_site, vaccination_site.start_date)

            return HttpResponseRedirect(f'/registrant/{registrant.pk}')

    context = {
        'address_form': address_form,
        'formset': formset,
    }

    return render(request, 'householdForm.html', context)


def CreateUserView(request, registrant):
    form = UserSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_registrant = True
            user.save()
            messages.info(request, "Account has been created. Register as an individual/household.")
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            if registrant == 'individual':
                return HttpResponseRedirect('/registrant/register/individual/')
            else:
                return HttpResponseRedirect('/registrant/register/household/')
    context = {
            'user_form': form,
    }

    return render(
        request, 'createUser.html', context
    )


def IndividualRegisterView(request):
    individual_form = IndividualRegistrantForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)
    if request.method == 'POST':

        if individual_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            coordinates = GetCoordinates(address)

            if coordinates:
                coordinates = coordinates[0]['geometry']['location']
                address.latitude = coordinates['lat']
                address.longitude = coordinates['lng']

            address.save()

            lgu_name = re.sub("[\(\[].*?[\)\]]", "", address.city).strip()

            lgu = LocalGovernmentUnit.objects.filter(name__contains=lgu_name)
            lgu = lgu[0] if lgu else None
            # Create registrant object
            registrant = Registrant(user=request.user, address=address, lgu=lgu)
            registrant.save()
            vaccination_site = DetermineVaccinationSite(registrant.pk)

            # Save link individual to registrant
            individual = individual_form.save(commit=False)
            individual.registrant = registrant
            individual.vaccination_site = vaccination_site
            individual.generateQR()
            individual.lgu = lgu
            individual.save()
            AssignPriorityGroup(individual)

            if vaccination_site:
                ScheduleAppointment(vaccination_site, vaccination_site.start_date)

            return HttpResponseRedirect(f'/registrant/{registrant.pk}')
        else:
            context = {
                'individual_form': individual_form,
                'address_form': address_form,
            }
    else:
        context = {
            'individual_form': individual_form,
            'address_form': address_form,
        }

    return render(
        request, 'individualForm.html', context
    )

