import os
from math import sqrt

from django.http import HttpResponse

from core.models import PriorityGroup
from registrant.models import Individual, Registrant


def DetermineVaccinationSite(registrant_id):
    registrant = Registrant.objects.get(pk=registrant_id)
    address = registrant.address
    lat = address.latitude
    lon = address.longitude

    # No available LGU
    if not registrant.lgu:
        return None

    vaccination_sites = registrant.lgu.vaccination_sites.all()
    if not vaccination_sites:
        return None

    distance = []
    for vs in vaccination_sites:
        vs_address = vs.address
        vs_lat = vs_address.latitude
        vs_lon = vs_address.longitude
        # Distance formula
        distance.append(sqrt((vs_lat - lat)**2 + (vs_lon - lon)**2))

    nearest_vs = vaccination_sites[distance.index(min(distance))]
    return nearest_vs


def AssignPriorityGroup(individual):
    """
    Crude way of auto priotization. Based on
    registration information. Could be improved
    with more comprehensive registration form.
    """
    comorbidities = (
        'cancer',
        'pregnant',
        'diabetes',
        'respiratory_illness',
        'cardiovascular_disease',
        'asthma',
        'high_blood_pressure',
        'organ_transplant',
        'kidney_disease',
        'sickle_cell_disease',
        'down_syndrome',
        'cerebrovascular_disease',
        'seizure_disorder',
        'blood_disease',
    )

    # optimize and reduce this soon
    # maybe iterate through each attribute
    if individual.is_frontline_worker:
        individual.priority_group = PriorityGroup.A1
        individual.save()
        return

    if individual.get_age() >= 60:
        individual.priority_group = PriorityGroup.A2
        individual.save()
        return

    for comorbidity in comorbidities:
        if getattr(individual, comorbidity):
            individual.priority_group = PriorityGroup.A3
            individual.save()
            return

    if individual.is_frontline_personnel or individual.is_uniformed_personnel:
        individual.priority_group = PriorityGroup.A4
        individual.save()
        return

    if individual.is_teacher_or_social_worker:
        individual.priority_group = PriorityGroup.B1
        individual.save()
        return

    if individual.is_government_worker:
        individual.priority_group = PriorityGroup.B2
        individual.save()
        return

    if individual.is_overseas_filipino_worker:
        individual.priority_group = PriorityGroup.B5
        individual.save()
        return

    if individual.is_employed:
        individual.priority_group = PriorityGroup.B6
        individual.save()
        return

    individual.priority_group = PriorityGroup.C
    individual.save()
