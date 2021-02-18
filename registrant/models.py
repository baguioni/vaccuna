from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class AddressField(models.Model):
    line1 = models.CharField('Street Address 1', max_length=50)
    line2 = models.CharField('Street Address 2', max_length=50, blank=True, default='')
    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField('City / Municipality', max_length=50)
    barangay = models.CharField(max_length=50)
    # TO DO
    # GOOGLE GEOLOC
    def get_formatted_address(self, sep='\n'):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(' '.join((self.barangay, self.city, self.province, self.region)))
        return sep.join((x.strip() for x in parts if x))

    def get_inline_address(self):
        return self.get_formatted_address(', ')

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
    address = models.ForeignKey('AddressField', on_delete=models.CASCADE)

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




