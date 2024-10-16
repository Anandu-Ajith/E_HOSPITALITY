from django.apps import AppConfig


class EHospitalityappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'e_hospitalityapp'

    def ready(self):
        import e_hospitalityapp.signals