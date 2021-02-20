from django.db import models
from core.models import AddressField


class LocalGovernmentUnit(models.Model):
    name = models.CharField(max_length=50)
    registrant_map = models.FileField(upload_to='maps/', null=True)


class VaccinationSite(models.Model):
    name = models.CharField(max_length=50)
    address = models.OneToOneField(AddressField, on_delete=models.CASCADE)
    lgu = models.ForeignKey(LocalGovernmentUnit, on_delete=models.CASCADE)
