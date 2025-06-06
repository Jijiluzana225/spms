# Generated by Django 5.1.2 on 2025-06-02 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0050_remove_employee_division_employee_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='division',
        ),
        migrations.AlterField(
            model_name='opcr',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='opcr.division'),
        ),
        migrations.AddField(
            model_name='employee',
            name='division',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='opcr.division'),
            preserve_default=False,
        ),
    ]
