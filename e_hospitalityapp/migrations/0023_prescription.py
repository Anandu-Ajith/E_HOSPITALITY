# Generated by Django 5.1.2 on 2024-10-15 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0022_remove_patientappointment_appointment_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicines', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_by_doctor', to='e_hospitalityapp.doctorprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_for_patient', to='e_hospitalityapp.patientprofile')),
            ],
        ),
    ]
