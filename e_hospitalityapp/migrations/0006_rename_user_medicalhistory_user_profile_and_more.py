# Generated by Django 5.1.2 on 2024-10-12 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0005_alter_medicalhistory_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalhistory',
            old_name='user',
            new_name='user_profile',
        ),
        migrations.RenameField(
            model_name='medicalinsurance',
            old_name='user',
            new_name='user_profile',
        ),
    ]