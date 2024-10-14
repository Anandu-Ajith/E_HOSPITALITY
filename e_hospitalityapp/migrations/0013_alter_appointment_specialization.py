# Generated by Django 5.1.2 on 2024-10-14 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0012_alter_appointment_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='e_hospitalityapp.doctorprofile'),
        ),
    ]