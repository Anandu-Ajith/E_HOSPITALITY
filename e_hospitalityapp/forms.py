from django import forms
from django.contrib.auth.models import User
from .models import MedicalHistory, MedicalInsurance, PatientProfile, PatientAppointment, Prescription


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
class DoctorRegistrationForm(forms.ModelForm):
    username= forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=15, required=True)
    specialization = forms.CharField(max_length=100, required=True)
    experience = forms.IntegerField(min_value=0, required=True)
    license_number = forms.CharField(max_length=100, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data


from django import forms
from django.contrib.auth.models import User
from .models import Administrator


class AdminRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=15, required=True)

    department = forms.CharField(max_length=100, required=True)
    position = forms.CharField(max_length=100, required=True)
    employee_id = forms.CharField(max_length=100, required=True)
    date_of_joining = forms.DateField(widget=forms.SelectDateWidget, required=True)
    profile_picture = forms.ImageField(required=False)

    # Address Fields
    address_line1 = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user


from .models import Facility

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'department', 'resource_name', 'resource_quantity', 'resource_available']


class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'gender', 'blood_group']



from .models import PatientProfile, MedicalHistory, MedicalInsurance

class PatientProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = PatientProfile
        fields = ['first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'blood_group']

    # Overriding the form's initialization to prepopulate user data
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user instance
        super(PatientProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'treatment', 'medications', 'allergies']

class MedicalInsuranceForm(forms.ModelForm):
    class Meta:
        model = MedicalInsurance
        fields = ['provider_name', 'policy_number', 'expiration_date', 'coverage_details']




from .models import Appointment, DoctorProfile


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['specialization', 'doctor', 'appointment_date', 'appointment_time_from', 'appointment_time_to']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time_from': forms.TimeInput(attrs={'type': 'time'}),
            'appointment_time_to': forms.TimeInput(attrs={'type': 'time'}),
        }

    specialization = forms.ChoiceField(choices=[], label="Specialization")

    doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.none(), label="Doctor")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        specializations = DoctorProfile.objects.values_list('specialization', flat=True).distinct()
        self.fields['specialization'].choices = [(spec, spec) for spec in specializations]

        if 'specialization' in self.data:
            try:
                specialization = self.data.get('specialization')
                self.fields['doctor'].queryset = DoctorProfile.objects.filter(specialization=specialization)
            except (ValueError, TypeError):
                self.fields['doctor'].queryset = DoctorProfile.objects.none()
        elif self.instance.pk:
            self.fields['doctor'].queryset = DoctorProfile.objects.filter(specialization=self.instance.specialization)
        else:
            self.fields['doctor'].queryset = DoctorProfile.objects.none()


class SelectDateForm(forms.Form):
    appointment_date = forms.DateField(widget=forms.SelectDateWidget)

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'treatment', 'medications', 'allergies']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'medicines']

    def __init__(self, *args, **kwargs):
            super(PrescriptionForm, self).__init__(*args, **kwargs)
            # Make doctor and patient fields read-only
            self.fields['doctor'].disabled = True
            self.fields['patient'].disabled = True


from django import forms
from django.contrib.auth.models import User
from .models import Administrator

class AdminEditForm(forms.ModelForm):
    # Fields for the User model
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    # Fields for the Administrator model
    department = forms.CharField(max_length=100)
    position = forms.CharField(max_length=100)
    employee_id = forms.CharField(max_length=50)
    date_of_joining = forms.DateField(widget=forms.SelectDateWidget())
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Administrator
        fields = ['department', 'position', 'employee_id', 'date_of_joining', 'profile_picture']  # Administrator fields only

    def save(self, commit=True):
        admin = super().save(commit=False)
        user = admin.user  # Get the related User object

        # Update the User fields
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Save User model
            admin.save()  # Save Administrator model

        return admin
