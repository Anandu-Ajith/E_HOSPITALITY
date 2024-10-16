from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from e_hospitalityapp.models import Administrator, loginTable

@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if not User.objects.filter(username='developer').exists():
        user = User.objects.create_superuser(
            username='developer',
            email='admin@example.com',
            password='adminpass',
            first_name='Admin',
            last_name='User'
        )

        administrator = Administrator.objects.create(
            user=user,
            department="Administration",
            position="Administrator",
            employee_id="EMP001",
            date_of_joining="2023-01-01",
            address_line1="123 Admin Street",
            city="Admin City",
            state="Admin State",
            postal_code="12345",
            country="Admin Country",
            is_approved=True
        )

        # Also create a loginTable entry
        login=loginTable.objects.create(
            username='developer',
            password='adminpass',
            password2='adminpass',
            type='admin'
        )

        login.save()
        administrator.save()