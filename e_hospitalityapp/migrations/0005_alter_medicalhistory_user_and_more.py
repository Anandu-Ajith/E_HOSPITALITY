# Generated by Django 5.1.2 on 2024-10-12 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0004_remove_userprofile_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalhistory',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='e_hospitalityapp.userprofile'),
        ),
        migrations.AlterField(
            model_name='medicalinsurance',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='e_hospitalityapp.userprofile'),
        ),
    ]