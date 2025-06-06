# Generated by Django 5.1.2 on 2025-01-21 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0044_division_cluster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcr_smart_kpi',
            name='first_half_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='opcr_smart_kpi',
            name='first_half_unit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='opcr_smart_kpi',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='opcr_smart_kpi',
            name='second_half_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='opcr_smart_kpi',
            name='second_half_unit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
