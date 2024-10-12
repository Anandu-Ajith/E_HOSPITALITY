from django import forms
from django.contrib.auth.models import User
from .models import MedicalHistory, MedicalInsurance


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'treatment', 'medications', 'allergies']


class MedicalInsuranceForm(forms.ModelForm):
    class Meta:
        model = MedicalInsurance
        fields = ['provider_name', 'policy_number', 'expiration_date', 'coverage_details']
