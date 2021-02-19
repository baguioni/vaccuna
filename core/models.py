from django.contrib.auth.models import AbstractUser
from django.db import models


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
    # TO DO
    # GOOGLE GEOLOC
    def get_formatted_address(self, sep='\n'):
        parts = [', '.join(filter(bool, [self.line1, self.line2]))]
        parts.append(' '.join((self.barangay, self.city, self.province, self.region)))
        return sep.join((x.strip() for x in parts if x))

    def get_inline_address(self):
        return self.get_formatted_address(', ')
