from registrant.models import Individual
from core.models import PriorityGroup


def AssignPriorityGroup(individual):
    comorbidities = (
        'cancer',
        'chronic_kidney_disease',
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
