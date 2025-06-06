# Generated by Django 5.1.2 on 2024-10-28 04:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['name'], 'verbose_name': 'Employee', 'verbose_name_plural': 'Employees'},
        ),
        migrations.AlterField(
            model_name='ipcr_opcr',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='opcr.employee'),
        ),
    ]
