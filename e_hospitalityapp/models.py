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



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=200)
    date_of_birth = models.DateField()
    # gender = models.TextField()
    password= models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
#   medical_history = models.TextField()
#     maritalStatus = models.CharField()
#   insurance_info = models.CharField(max_length=200)
    def __str__(self):
        return '{}'.format(self.username)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    medications = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History of {self.user.username}"

class MedicalInsurance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    expiration_date = models.DateField()
    coverage_details = models.TextField()

    def __str__(self):
        return f"Insurance of {self.user.username}"