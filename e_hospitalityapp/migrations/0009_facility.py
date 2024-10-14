# Generated by Django 5.1.2 on 2024-10-13 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_hospitalityapp', '0008_administrator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=100)),
                ('resource_name', models.CharField(max_length=100)),
                ('resource_quantity', models.PositiveIntegerField()),
                ('resource_available', models.BooleanField(default=True)),
            ],
        ),
    ]