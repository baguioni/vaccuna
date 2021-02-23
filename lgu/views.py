from django.shortcuts import render
from lgu.models import LocalGovernmentUnit
from lgu.tasks import generate_registrant_markers_map

def DashboardView(request, lgu_id):
    obj = LocalGovernmentUnit.objects.get(id=lgu_id)
    first_dose = obj.individuals.filter(vaccination_status=1).count()
    fully_vaccinated = obj.individuals.filter(vaccination_status=2).count()
    # generate_registrant_markers_map(obj)
    context = {
        'obj': obj,
        'fully_vaccinated': fully_vaccinated,
        'first_dose': first_dose
    }
    return render(request, "lguDashboard.html", context)

