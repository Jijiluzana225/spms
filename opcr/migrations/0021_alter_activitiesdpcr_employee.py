# Generated by Django 5.1.2 on 2024-10-30 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0020_alter_ipcr_dpcr_name_alter_ipcr_dpcr_smart_kpi_dpcr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitiesdpcr',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ActivitiesDPCR', to='opcr.employee'),
        ),
    ]
