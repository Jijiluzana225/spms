# Generated by Django 5.1.2 on 2024-11-13 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0031_employee_designation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitiesdpcr',
            old_name='DPCR_kpi',
            new_name='dpcr_kpi',
        ),
    ]
