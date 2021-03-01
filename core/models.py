import qrcode
import cv2 as cv
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
import googlemaps
from enum import IntEnum
import requests


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


# GENEREATE AND READ QR


class QR(models.Model):
    name = models.CharField(max_length=250)
    qr_code = models.ImageField(upload_to=None)

    def __str__(self):
        return str(self.name)

    def generateQR(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.name)  # data here
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        # image overlay code start (remove if not needed)
        logo_display = Image.open('Vaccuna Logo.png')
        logo_display.thumbnail((150, 150))
        logo_pos = ((img.size[0] - logo_display.size[0]) // 2,
                    (img.size[1] - logo_display.size[1]) // 2)
        img.paste(logo_display, logo_pos)
        # image overlay code end
        # img.save("qr00001.png")
        return img

    def readQR(img):
        im = cv.imread('sample2.png')
        det = cv.QRCodeDetector()
        retval, points, straight_qrcode = det.detectAndDecode(im)
        # result is stored in retval ,return retval
        return retval
# GENEREATE AND READ QR

# my_num = "+639470676215"  -> sample number, number is declared as string not int
#my_message = "Good day Juan Dela Cruz! This is to inform you of your scheduled vaccination on March 2, 2021 at PGH. Addt'l reminders here"
#sms(my_num, my_message)


def sms(number, message):
    url = "https://rest-api.d7networks.com/secure/send"
    payload = "{\n\t\"to\":\"%s\",\n\t\"content\": \" %s \", \n\t\"from\": \"Vaccuna\", \n\t\"dlr\": \"yes\", \n\t\"dlr-method\": \"GET\", \n\t\"dlr-level\": \"2\", \n\t\"dlr-url\": \"http://yourcustompostbackurl.com\"\n}" % (
        number, message)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic dWZsbjM2MTU6VXVmdk9XSno='
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload)  # get api respons
    # print(response.text.encode('utf8'))  # prints api response(success or not)
    return


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_registrant = models.BooleanField(default=False)


class AddressField(models.Model):
    line1 = models.CharField('Street Address 1', max_length=50)
    line2 = models.CharField(
        'Street Address 2', max_length=50, blank=True, default='')
    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField('City / Municipality', max_length=50)
    barangay = models.CharField(max_length=50)
    line1 = models.CharField('Street Address 1', max_length=50)
    line2 = models.CharField(
        'Street Address 2', max_length=50, blank=True, default='', null=True)
    latitude = models.DecimalField(
        max_digits=18, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=18, decimal_places=15, null=True, blank=True)

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
