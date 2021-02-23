from django.contrib.auth.models import AbstractUser
from django.db import models
import googlemaps
from enum import IntEnum


class PriorityGroup(IntEnum):
    """
    Based from DOH
    # https://www.rappler.com/nation/philippine-government-releases-new-vaccine-priority-list-includes-persons-with-comorbidities
    """
    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4
    A5 = 5
    B1 = 6
    B2 = 7
    B3 = 8
    B4 = 9
    B5 = 10
    B6 = 11
    C = 12


    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_registrant = models.BooleanField(default=False)


class AddressField(models.Model):
    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField('City / Municipality', max_length=50)
    barangay = models.CharField(max_length=50)
    line1 = models.CharField('Street Address 1', max_length=50)
    line2 = models.CharField('Street Address 2', max_length=50, blank=True, default='', null=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)


    def get_formatted_address(self):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(', '.join((self.barangay, self.city, self.province)))
        return ' '.join((x.strip() for x in parts if x))

    def get_full_address(self):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(', '.join((self.barangay, self.city, self.province, self.region)))
        return ' '.join((x.strip() for x in parts if x))

    def get_inline_address(self):
        return self.get_full_address()

    def get_coordinates(self):
        return (self.latitude, self.longitude)
