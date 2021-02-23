from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from core.models import AddressField, User, PriorityGroup
from lgu.models import LocalGovernmentUnit
from django.utils.translation import gettext_lazy as _


class Registrant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.OneToOneField(AddressField, on_delete=models.CASCADE, null=True)
    is_household = models.BooleanField(default=False)
    lgu = models.ForeignKey(LocalGovernmentUnit, related_name='registrants', on_delete=models.CASCADE, null=True)


class Individual(models.Model):

    class ChecklistChoice(models.TextChoices):
        YES = 'YES', _('Yes')
        NO = 'NO', _('No')
        NOT_SURE = 'NS', _('Not sure')

    class Status(models.TextChoices):
        GRANTED = 'G', _('Granted')
        DENIED = 'D', _('Denied')
        WAITLISTED = 'W', _('Waitlisted')
        PENDING = 'P', _('Pending')

    # Basic Info
    first_name = models.CharField(max_length=50, )
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    mobile_number = PhoneNumberField()
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE)

    # Living Situation
    had_covid = models.CharField(
        max_length=3,
        choices=ChecklistChoice.choices,
        default=ChecklistChoice.NO,
    )
    live_with_covid = models.CharField(
        max_length=3,
        choices=ChecklistChoice.choices,
        default=ChecklistChoice.NO,
    )

    # Vaccination status/info
    registration_status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PENDING,
    )

    vaccination_status = models.IntegerField(default=0)
    vaccination_site = models.ForeignKey(AddressField, on_delete=models.CASCADE, null=True)
    first_vaccination_datetime = models.DateTimeField(null=True)
    second_vaccination_datetime = models.DateTimeField(null=True)

    # Employment status
    is_frontline_worker = models.BooleanField(default=False)
    is_frontline_personnel = models.BooleanField(default=False)
    is_uniformed_personnel = models.BooleanField(default=False)
    is_teacher_or_social_worker = models.BooleanField(default=False)
    is_government_worker = models.BooleanField(default=False)
    is_overseas_filipino_worker = models.BooleanField(default=False)
    is_employed = models.BooleanField(default=False)

    # co-morbidities
    # https://www.cdc.gov/coronavirus/2019-ncov/need-extra-precautions/people-with-medical-conditions.html    cancer = models.BooleanField(default=False)
    # https://www.uppi.upd.edu.ph/sites/default/files/pdf/COVID-19-Research-Brief-01.pdf
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7306563/
    cancer = models.BooleanField(default=False)
    chronic_kidney_disease = models.BooleanField(default=False)
    pregnant = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    respiratory_illness = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    organ_transplant = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    sickle_cell_disease = models.BooleanField(default=False)
    down_syndrome = models.BooleanField(default=False)
    cerebrovascular_disease = models.BooleanField(default=False)
    seizure_disorder = models.BooleanField(default=False)
    blood_disease = models.BooleanField(default=False)
    priority_group = models.IntegerField(choices=PriorityGroup.choices(), default=PriorityGroup.C)


    def get_full_name(self):
        full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return full_name.strip()

    def get_age(self):
        today = date.today()
        birthday = self.birthday
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
