# Generated by Django 5.1.2 on 2025-05-19 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0047_alter_opcr_smart_kpi_remarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opcr',
            name='division',
        ),
        migrations.AddField(
            model_name='opcr',
            name='division',
            field=models.ManyToManyField(to='opcr.division'),
        ),
    ]
