from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender= models.TextField()
#     medical_history = models.TextField()
#     insurance_info = models.CharField(max_length=200)



class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    # gender = models.TextField()
#     maritalStatus = models.CharField()
    # blood group
    def __str__(self):
        return '{}'.format(self.user)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()  # for storing years of experience
    license_number = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

class loginTable(models.Model):
    username=models.CharField(max_length=200)
    # date_of_birth = models.DateField()
    # gender = models.TextField()
    password= models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
#   medical_history = models.TextField()
#   insurance_info = models.CharField(max_length=200)
    type=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)

from django.db import models
from django.contrib.auth.models import User

class MedicalHistory(models.Model):
    user_profile = models.OneToOneField(PatientProfile, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    medications = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History of {self.user_profile.user.username}"

class MedicalInsurance(models.Model):
    user_profile = models.OneToOneField(PatientProfile, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    expiration_date = models.DateField()
    coverage_details = models.TextField()

    def __str__(self):
        return f"Insurance of {self.user_profile.user.username}"





class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100, unique=True)
    date_of_joining = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"


class Facility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    resource_name = models.CharField(max_length=100)
    resource_quantity = models.PositiveIntegerField()
    resource_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.department}'