from django import forms
from django.forms import ModelForm, SelectDateWidget
from registrant.models import Individual
from registrant.models import AddressField

class AddressFieldForm(ModelForm):
    class Meta:
      model = AddressField
      fields = '__all__'

    line1 = forms.CharField(initial='Street Address 1')
    line2 = forms.CharField(initial='Street Address 2')
    region = forms.CharField(label=('Region'),
                  widget=forms.Select(attrs={'id': 'region'}),
                  required=False,
                )
    province = forms.CharField(label=('Province'),
                  widget=forms.Select(attrs={'id': 'province'}),
                  required=False,
                )
    city = forms.CharField(label=('City/Municipality'),
                  widget=forms.Select(attrs={'id': 'city'}),
                  required=False,
                )
    barangay = forms.CharField(label=('Barangay'),
                  widget=forms.Select(attrs={'id': 'barangay'}),
                  required=False,
                )


class IndividualRegistrantForm(ModelForm):
    class Meta:
        model = Individual
        exclude = ('address',)

        widgets = {
            'birthday' : SelectDateWidget(),
        }
