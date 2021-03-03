from django.shortcuts import redirect, render

from lgu.forms import PriorityLocationForm, VaccinationSiteForm
from lgu.models import LocalGovernmentUnit, PriorityLocation, VaccinationSite
from lgu.tasks import generate_registrant_markers_map
from registrant.forms import AddressFieldForm


def DashboardView(request, lgu_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    obj = LocalGovernmentUnit.objects.get(pk=lgu_id)
    first_dose = obj.individuals.filter(vaccination_status=1).count()
    fully_vaccinated = obj.individuals.filter(vaccination_status=2).count()
    template = "lguDashboard.html"
    if request.user.id != obj.user.id:
        template = "allow.html"
    generate_registrant_markers_map(obj)
    context = {
        'obj': obj,
        'fully_vaccinated': fully_vaccinated,
        'first_dose': first_dose
    }
    return render(request, template, context)


def VaccinationSiteView(request, vs_id, lgu_id):
    vs = VaccinationSite.objects.get(pk=vs_id)
    individuals = vs.individuals.all().order_by('priority_group')
    dates = vs.individuals.all().values_list('first_vaccination_datetime', flat=True).distinct()
    # dates = [f'{date.strftime("%B")} {date.strftime("%d")}, {date.strftime("%Y")}' for date in dates]
    context = {
        "obj": vs,
        'individuals': individuals,
        # 'dates': dates,
    }

    return render(request, 'vaccinationSiteView.html', context)


def VaccinationSiteCreate(request, lgu_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    site_form = VaccinationSiteForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)
    lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)

    if request.method == 'POST':
        if site_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            site = site_form.save(commit=False)
            site.address = address
            site.lgu = lgu
            site.save()
            return redirect(f'/lgu/{lgu.pk}')

    context = {
        'site_form': site_form,
        'address_form': address_form,
        'lgu': lgu,
    }
    return render(request, "vaccinationSite.html", context)

def VaccinationSiteUpdate(request, lgu_id, vs_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    vs = VaccinationSite.objects.get(pk=vs_id)
    address = vs.address
    site_form = VaccinationSiteForm(request.POST or None, instance=vs)
    address_form = AddressFieldForm(request.POST or None, instance=address)
    lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)

    if request.method == 'POST':
        if site_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            site = site_form.save(commit=False)
            site.address = address
            site.lgu = lgu
            site.save()
            return redirect(f'/lgu/{lgu.pk}')

    context = {
        'site_form': site_form,
        'address_form': address_form,
        'lgu': lgu,
    }
    return render(request, "vaccinationSite.html", context)


def VaccinationSiteDelete(request, lgu_id, vs_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    obj = VaccinationSite.objects.get(id=vs_id)
    if request.method == 'POST':
        obj.delete()
        return redirect(f'/lgu/{lgu_id}')
    context = {
        'obj': obj,
        'lgu_id': lgu_id
    }
    return render(request, "deleteLGU.html", context)


def PriorityLocationCreate(request, lgu_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    priority_form = PriorityLocationForm(request.POST or None)
    address_form = AddressFieldForm(request.POST or None)
    lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)

    if request.method == 'POST':

        if priority_form.is_valid() and address_form.is_valid():
            ddress = address_form.save()
            priority = priority_form.save(commit=False)
            priority.lgu = lgu
            priority.address = address
            priority.save()
            return redirect(f'/lgu/{lgu.pk}')

    context = {
        'priority_form': priority_form,
        'address_form': address_form,
        'lgu': lgu,
    }

    return render(request, "priorityLocation.html", context)


def PriorityLocationUpdate(request, lgu_id, pl_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    pl = PriorityLocation.objects.get(pk=pl_id)
    address = pl.address
    priority_form = PriorityLocationForm(request.POST or None, instance=pl)
    address_form = AddressFieldForm(request.POST or None, instance=address)
    lgu = LocalGovernmentUnit.objects.get(pk=lgu_id)

    if request.method == 'POST':

        if priority_form.is_valid() and address_form.is_valid():
            ddress = address_form.save()
            priority = priority_form.save(commit=False)
            priority.lgu = lgu
            priority.address = address
            priority.save()
            return redirect(f'/lgu/{lgu.pk}')

    context = {
        'priority_form': priority_form,
        'address_form': address_form,
        'lgu': lgu,
    }

    return render(request, "priorityLocation.html", context)


def PriorityLocationDelete(request, lgu_id, pl_id):
    if not request.user.is_lgu:
        return render(request, "allow.html", {})
    obj = PriorityLocation.objects.get(id=pl_id)
    if request.method == 'POST':
        obj.delete()
        return redirect(f'/lgu/{lgu_id}')
    context = {
        'obj': obj,
        'lgu_id': lgu_id
    }
    return render(request, "deleteLGU.html", context)
