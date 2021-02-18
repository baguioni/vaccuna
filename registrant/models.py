from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import AddressField, User


class Registrant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.OneToOneField(AddressField, on_delete=models.CASCADE)
    is_household = models.BooleanField(default=False)

class Individual(models.Model):
    YES = 'YES'
    NO = 'NO'
    NOT_SURE = 'NOT_SURE'

    CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
        (NOT_SURE, 'Not sure')
    ]

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateTimeField()
    mobile_number = PhoneNumberField()
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE)

    # Checklist
    had_covid = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=NOT_SURE,
    )

    live_with_covid = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=NOT_SURE,
    )

    # Symptoms

    # Sickness
    respiratory_illness = models.BooleanField()
    cardiovascular_illness = models.BooleanField()
    asthma = models.BooleanField()
    kidney_stones = models.BooleanField()
    diabetes = models.BooleanField()
    high_blood_pressure = models.BooleanField()
    blood_disease = models.BooleanField()
    cancer = models.BooleanField()
    leukemia = models.BooleanField()
    organ_transplant = models.BooleanField()
    pregnant = models.BooleanField()
    currently_employed = models.BooleanField()

    def get_full_name(self):
        full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return full_name.strip()




