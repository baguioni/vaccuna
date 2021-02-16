from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Individual(models.Model):
    # https://psa.gov.ph/classification/psgc/
    # address ^

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
    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    barangay = models.CharField(max_length=50)


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
