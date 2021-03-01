from django import forms
from django.forms import ModelForm
from lgu.models import VaccinationSite, PriorityLocation


class VaccinationSiteForm(ModelForm):
    class Meta:
        model = VaccinationSite
        exclude = ('lgu', 'address',)


class PriorityLocationForm(ModelForm):
    class Meta:
        model = PriorityLocation
        fields = ('name', )
