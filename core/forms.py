from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import User


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'password1': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'password2': forms.TextInput(attrs={'class': 'form-control form-control-lg'})
        }

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
