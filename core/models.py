from django.contrib.auth.models import AbstractUser
from django.db import models
import qrcode
from PIL import Image
import cv2 as cv
import googlemaps
from enum import IntEnum

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


class sms(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        pass


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
    line1 = models.CharField('Street Address 1', max_length=50)
    line2 = models.CharField(
        'Street Address 2', max_length=50, blank=True, default='')

    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    city = models.CharField('City / Municipality', max_length=50)
    barangay = models.CharField(max_length=50)

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
