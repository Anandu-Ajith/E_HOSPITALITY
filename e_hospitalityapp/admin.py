from django.contrib import admin

from e_hospitalityapp.models import Patient, UserProfile, loginTable

# Register your models here.
admin.site.register(Patient)
admin.site.register(UserProfile)
admin.site.register(loginTable)
