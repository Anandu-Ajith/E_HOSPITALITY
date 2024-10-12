from django.contrib import admin

from e_hospitalityapp.models import Patient, UserProfile, loginTable, MedicalHistory, MedicalInsurance

# Register your models here.
admin.site.register(Patient)
admin.site.register(UserProfile)
admin.site.register(loginTable)
admin.site.register(MedicalInsurance)
admin.site.register(MedicalHistory)
