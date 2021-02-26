from django import forms
from django.forms import ModelForm, SelectDateWidget, modelformset_factory

from core.models import AddressField, User
from registrant.models import Individual, Registrant

class DateInput(forms.DateInput):
    input_type = 'date'

class AddressFieldForm(ModelForm):
    class Meta:
        model = AddressField
        exclude = ('longitude', 'latitude')

        widgets = {
            'line1': forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            'line2': forms.TextInput(attrs={"class": "form-control form-control-lg"}),
            'region': forms.Select(attrs={'id': 'region', 'class': 'form-control form-control-lg'}),
            'province': forms.Select(attrs={'id': 'province', 'class': 'form-control form-control-lg'}),
            'city': forms.Select(attrs={'id': 'city', 'class': 'form-control form-control-lg'}),
            'barangay': forms.Select(attrs={'id': 'barangay', 'class': 'form-control form-control-lg'})
        }


class IndividualRegistrantForm(ModelForm):
    class Meta:
        model = Individual
        exclude = (
          'registrant',
          'registration_status',
          'vaccination_status',
          'first_vaccination_datetime',
          'second_vaccination_datetime',
          'vaccination_site',
          'priority_group',
          'lgu',
          'qrcode'
          )

        widgets = {
            'birthday': DateInput(attrs={'class': 'form-control'}),
        }


IndividualFormset = modelformset_factory(
    Individual,
    form=IndividualRegistrantForm
)
