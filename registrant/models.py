from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from core.models import AddressField, User
from lgu.models import LocalGovernmentUnit
from django.utils.translation import gettext_lazy as _


class Registrant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.OneToOneField(AddressField, on_delete=models.CASCADE)
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
    first_name = models.CharField(max_length=50)
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
    is_employed = models.BooleanField(default=False)
    is_uniformed_personnel = models.BooleanField(default=False)
    is_healthcare_worker = models.BooleanField(default=False)

    # Medical History
    respiratory_illness = models.BooleanField(default=False)
    cardiovascular_illness = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    kidney_stones = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    blood_disease = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    leukemia = models.BooleanField(default=False)
    organ_transplant = models.BooleanField(default=False)
    pregnant = models.BooleanField(default=False)

    def get_full_name(self):
        full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return full_name.strip()

    def get_age(self):
        today = date.today()
        birthday = self.birthday
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
