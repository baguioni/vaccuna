from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from core.models import AddressField, User, PriorityGroup
from lgu.models import LocalGovernmentUnit
from django.utils.translation import gettext_lazy as _
from lgu.models import VaccinationSite
import qrcode
from vaccuna import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile


class Registrant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.OneToOneField(AddressField, on_delete=models.CASCADE, null=True)
    is_household = models.BooleanField(default=False)
    lgu = models.ForeignKey(LocalGovernmentUnit, related_name='registrants', on_delete=models.PROTECT, null=True)


class Individual(models.Model):

    class ChecklistChoice(models.TextChoices):
        YES = 'YES', _('Yes')
        NO = 'NO', _('No')
        NOT_SURE = 'NS', _('Not sure')


    class SexAtBirth(models.TextChoices):
        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')


    class Status(models.TextChoices):
        GRANTED = 'G', _('Granted')
        DENIED = 'D', _('Denied')
        WAITLISTED = 'W', _('Waitlisted')
        PENDING = 'P', _('Pending')

    # Basic Info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)

    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    sex_assigned_at_birth = models.CharField(
        max_length=6,
        choices=SexAtBirth.choices,
        default=None,
        null=True
    )
    mobile_number = PhoneNumberField()
    registrant = models.ForeignKey(Registrant, on_delete=models.CASCADE, related_name='individuals')
    lgu = models.ForeignKey(LocalGovernmentUnit, related_name='individuals', on_delete=models.PROTECT, null=True)

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
    vaccination_site = models.ForeignKey(VaccinationSite, on_delete=models.PROTECT, null=True, related_name='individuals')
    first_vaccination_datetime = models.DateField(null=True)
    second_vaccination_datetime = models.DateField(null=True)

    # Employment status
    is_frontline_worker = models.BooleanField(default=False)
    is_frontline_personnel = models.BooleanField(default=False)
    is_uniformed_personnel = models.BooleanField(default=False)
    is_teacher_or_social_worker = models.BooleanField(default=False)
    is_government_worker = models.BooleanField(default=False)
    is_overseas_filipino_worker = models.BooleanField(default=False)
    is_employed = models.BooleanField(default=False)

    # co-morbidities
    # https://www.cdc.gov/coronavirus/2019-ncov/need-extra-precautions/people-with-medical-conditions.html
    # https://www.uppi.upd.edu.ph/sites/default/files/pdf/COVID-19-Research-Brief-01.pdf
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7306563/
    cancer = models.BooleanField(default=False)
    pregnant = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    respiratory_illness = models.BooleanField(default=False)
    cardiovascular_disease = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    organ_transplant = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    sickle_cell_disease = models.BooleanField(default=False)
    down_syndrome = models.BooleanField(default=False)
    cerebrovascular_disease = models.BooleanField(default=False)
    seizure_disorder = models.BooleanField(default=False)
    blood_disease = models.BooleanField(default=False)
    priority_group = models.IntegerField(choices=PriorityGroup.choices(), null=True)

    qr_code = models.ImageField(upload_to='QRCodes/', null=True, blank=True)


    def get_full_name(self):
        full_name = f'{self.first_name} {self.middle_name} {self.last_name}'
        return full_name.strip()


    def get_age(self):
        today = date.today()
        birthday = self.birthday
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


    def generateQR(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=40,
            border=8,
        )
        qr.add_data(settings.BASE_URL+'/api/qrcode/'+str(self.id))  # data here
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        # image overlay code start (remove if not needed)
        logo_display = Image.open('Vaccuna Logo.png')
        logo_display.thumbnail((150, 150))
        logo_pos = ((img.size[0] - logo_display.size[0]) // 2,
                    (img.size[1] - logo_display.size[1]) // 2)
        img.paste(logo_display, logo_pos)
        temp = BytesIO()
        img.save(fp=temp, format='JPEG')
        image_file = ContentFile(temp.getvalue())
        file_name = 'QR-'+self.get_full_name()+'.jpeg'

        self.qr_code.save(file_name, InMemoryUploadedFile(
             image_file,       # file
             None,               # field_name
             file_name,           # file name
             'image/jpeg',       # content_type
             image_file.tell,  # size
             None)               # content_type_extra
        )
