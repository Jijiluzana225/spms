# Generated by Django 5.1.2 on 2024-11-19 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0033_opcr_smart_kpi_averagescore_opcr_smart_kpi_budget_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcr_smart_kpi',
            name='assignedto',
            field=models.ManyToManyField(to='opcr.employee'),
        ),
    ]
