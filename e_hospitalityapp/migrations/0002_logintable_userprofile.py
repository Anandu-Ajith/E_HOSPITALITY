# Generated by Django 5.1.2 on 2024-10-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='loginTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.TextField()),
                ('password', models.CharField(max_length=200)),
                ('password2', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.TextField()),
                ('password', models.CharField(max_length=200)),
                ('password2', models.CharField(max_length=200)),
            ],
        ),
    ]