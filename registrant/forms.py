from django import forms
from django.forms import ModelForm, SelectDateWidget, modelformset_factory

from core.models import AddressField, User
from registrant.models import Individual


class AddressFieldForm(ModelForm):
    class Meta:
        model = AddressField
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
        }

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
        exclude = ('registrant',)

        widgets = {
            'birthday' : SelectDateWidget(),
        }


IndividualFormset = modelformset_factory(
    Individual,
    form=IndividualRegistrantForm
)
