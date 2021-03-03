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
    def __init__(self, *args, **kwargs):
        super(IndividualRegistrantForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].initial = '+63'

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
          'qr_code',
          )

        widgets = {
            'birthday': DateInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'had_covid': 'Did/do you have COVID-19?',
            'live_with_covid': 'Do you live with someone who had/have COVID-19?',
            'cancer': 'Do you have Cancer?',
            'pregnant': 'Are you pregnant or have plans?',
            'diabetes': 'Do you have Diabetes?',
            'respiratory_illness': 'Do you have Respiratory Illness?',
            'cardiovascular_disease': 'Do you have Cardiovascular Disease?',
            'asthma': 'Do you have Severe Asthma?',
            'high_blood_pressure': 'Do you have High Blood Pressure?',
            'organ_transplant': 'Do you have an Organ Transplant?',
            'kidney_disease': 'Do you have Kidney Disease?',
            'sickle_cell_disease': 'Do you have Sickle Cell Disease?',
            'down_syndrome': 'Do you have Down Syndrome?',
            'cerebrovascular_disease': 'Do you have Cerebrovascular Disease?',
            'seizure_disorder': 'Do you have Seizure Disorder?',
            'blood_disease': 'Do you have Blood Disease?',
            'is_frontline_worker': 'Are you a Frontline Worker in a health facility?',
            'is_frontline_personnel': 'Are you a Frontline Personnel?',
            'is_uniformed_personnel':  'Are you a Uniformed Personnel? ',
            'is_teacher_or_social_worker': 'Are you a Teacher(public or private) or Social Worker?',
            'is_government_worker': 'Are you a Government Worker?',
            'is_overseas_filipino_worker':  'Are you an Overseas Filipino Worker?',
            'is_employed': 'Are you Employed?',
        }


IndividualFormset = modelformset_factory(
    Individual,
    form=IndividualRegistrantForm
)
