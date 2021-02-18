from django.contrib.auth.models import AbstractUser
from django.db import models
import googlemaps


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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def get_formatted_address(self):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(', '.join((self.barangay, self.city, self.province)))
        return ' '.join((x.strip() for x in parts if x))

    def get_full_address(self):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(', '.join((self.barangay, self.city, self.province, self.region)))
        return ' '.join((x.strip() for x in parts if x))

    def get_inline_address(self):
        return self.get_full_address(', ')

    def get_coordinates(self):
        return (self.latitude, self.longitude)
