from django.shortcuts import render
from lgu.models import LocalGovernmentUnit, VaccinationSite, PriorityLocation
from lgu.tasks import generate_registrant_markers_map
from lgu.forms import VaccinationSiteForm, PriorityLocationForm
from registrant.forms import AddressFieldForm

def DashboardView(request, lgu_id):
    obj = LocalGovernmentUnit.objects.get(pk=lgu_id)
    first_dose = obj.individuals.filter(vaccination_status=1).count()
    fully_vaccinated = obj.individuals.filter(vaccination_status=2).count()
    # generate_registrant_markers_map(obj)
    context = {
        'obj': obj,
        'fully_vaccinated': fully_vaccinated,
        'first_dose': first_dose
    }
    return render(request, "lguDashboard.html", context)

def VaccinationSiteCreate(request, lgu_id):
    site_form = VaccinationSiteForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)

    if request.method == 'POST':
        if site_form.valid() and address_form.valid():
            address_form.save()
            lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)
            site = site_form.save(lgu=lgu)

    context = {
        'site_form': site_form,
        'address_form': address_form,
    }
    return render(request, "lguDashboard.html", context)

def PriorityLocationCreate(request, lgu_id):
    priority_form = PriorityLocationForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)

    if request.method == 'POST':
        if priority_form.valid() and address_form.valid():
            address_form.save()
            lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)
            priority = priority_form.save(lgu=lgu)

    context = {
        'priority_form': priority_form,
        'address_form': address_form,
    }

    return render(request, "lguDashboard.html", context)
