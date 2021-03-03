from enum import IntEnum

import googlemaps
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import requests


class sms(models.Model):
    number = models.CharField(max_length=13)
    message = models.CharField(max_length=250)

    def __str__(self):
        return str(self.number, self.message)

    def save(self, *args, **kwargs):
        # my_num = "+639470676215"  -> sample number, number is declared as string not int
        #my_message = "Good day Juan Dela Cruz! This is to inform you of your scheduled vaccination on March 2, 2021 at PGH. Addt'l reminders here"
        url = "https://rest-api.d7networks.com/secure/send"
        payload = "{\n\t\"to\":\"%s\",\n\t\"content\": \" %s \", \n\t\"from\": \"Vaccuna\", \n\t\"dlr\": \"yes\", \n\t\"dlr-method\": \"GET\", \n\t\"dlr-level\": \"2\", \n\t\"dlr-url\": \"http://yourcustompostbackurl.com\"\n}" % (
            self.number, self.message)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic dWZsbjM2MTU6VXVmdk9XSno='
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload)  # get api respons
        # prints api response(success or not)
        print(response.text.encode('utf8'))
        return


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
    is_lgu = models.BooleanField(default=False)
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
        parts.append(
            ', '.join((self.barangay, self.city, self.province, self.region)))
        return ' '.join((x.strip() for x in parts if x))

    def get_inline_address(self):
        return self.get_full_address()

    def get_coordinates(self):
        return (self.latitude, self.longitude)
