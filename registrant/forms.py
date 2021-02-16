from django import forms
from django.forms import ModelForm, SelectDateWidget
from registrant.models import Individual

class IndividualRegistrantForm(ModelForm):
    class Meta:
        model = Individual
        fields = '__all__'

        widgets = {
            'birthday' : SelectDateWidget(),
        }

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
