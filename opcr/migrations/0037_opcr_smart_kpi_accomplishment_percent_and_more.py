# Generated by Django 5.1.2 on 2024-11-27 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0036_opcr_smart_kpi_budget_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcr_smart_kpi',
            name='accomplishment_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='opcr_smart_kpi',
            name='accomplishment_qty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
