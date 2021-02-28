from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from core.forms import UserSignupForm
from registrant.forms import (AddressFieldForm, IndividualFormset,
                              IndividualRegistrantForm)
from registrant.models import Individual, Registrant
import googlemaps
from django.conf import settings
from registrant.tasks import AssignPriorityGroup
from core.tasks import GetCoordinates
import re
from lgu.models import LocalGovernmentUnit

from django.shortcuts import render
from wsgiref.util import FileWrapper
import os

def DownloadQRCode(request, id):
    img = Individual.objects.get(pk=id).qr_code
    filename = os.path.basename(img.file.name)
    response = HttpResponse(img.file, content_type='image/jpeg')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def RegistrantDashboard(request, id):
    registrant = Registrant.objects.get(pk=id)
    individuals = registrant.individuals.all()
    context = {
        'registrant': registrant,
        'individuals': individuals
    }
    return render(request, "home.html", context)


def HouseholdRegisterView(request):
    if request.method == "GET":
        user_form = UserSignupForm(request.GET or None)
        address_form = AddressFieldForm(request.GET or None)
        formset = IndividualFormset(queryset=Individual.objects.none())

    if request.method == "POST":

        user_form = UserSignupForm(request.POST)
        address_form = AddressFieldForm(request.POST or None)
        formset = IndividualFormset(request.POST)

        if formset.is_valid() and address_form.is_valid() and user_form.is_valid():
            address = address_form.save()
            coordinates = GetCoordinates(address)


            if coordinates:
                coordinates = coordinates[0]['geometry']['location']
                address.latitude = coordinates['lat']
                address.longitude = coordinates['lng']

            address.save()

            user = user_form.save(commit=False)
            user.is_registrant = True
            user.save()

            lgu_name = re.sub("[\(\[].*?[\)\]]", "", address.city).strip()

            lgu = LocalGovernmentUnit.objects.filter(name__contains=lgu_name)
            lgu = lgu if lgu else None
            # Create registrant object
            registrant = Registrant(user=user, address=address, is_household=True, lgu=lgu)
            registrant.save()

            for individual_form in formset:
                if individual_form.is_valid():
                    try:
                        individual = individual_form.save(commit=False)
                        individual.registrant = registrant
                        individual.generateQR()
                        individual.lgu = lgu
                        individual.save()
                        AssignPriorityGroup(individual)

                    except:
                        print('database error')

            return HttpResponseRedirect(f'/registrant/{registrant.pk}')

    context = {
        'user_form': user_form,
        'address_form': address_form,
        'formset': formset,

    }

    return render(request, 'householdForm.html', context)

def IndividualRegisterView(request):
    individual_form = IndividualRegistrantForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)
    user_form = UserSignupForm(request.POST or None)
    if request.method == 'POST':

        if individual_form.is_valid() and address_form.is_valid() and user_form.is_valid():
            address = address_form.save()
            coordinates = GetCoordinates(address)
            if coordinates:
                coordinates = coordinates[0]['geometry']['location']
                address.latitude = coordinates['lat']
                address.longitude = coordinates['lng']

            address.save()

            user = user_form.save(commit=False)
            user.is_registrant = True
            user.save()

            lgu_name = re.sub("[\(\[].*?[\)\]]", "", address.city).strip()

            lgu = LocalGovernmentUnit.objects.filter(name__contains=lgu_name)
            lgu = lgu if lgu else None
            # Create registrant object
            registrant = Registrant(user=user, address=address, lgu=lgu)
            registrant.save()

            # Save link individual to registrant
            individual = individual_form.save(commit=False)
            individual.registrant = registrant
            individual.generateQR()
            individual.lgu = lgu
            individual.save()
            AssignPriorityGroup(individual)

            return HttpResponseRedirect(f'/registrant/{registrant.pk}')
        else:
            context = {
                'individual_form': individual_form,
                'address_form': address_form,
                'user_form': user_form,
            }
    else:
        context = {
            'individual_form': individual_form,
            'address_form': address_form,
            'user_form': user_form,
        }

    return render(
        request, 'individualForm.html', context
    )

