# Generated by Django 5.1.2 on 2024-10-29 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0010_opcr'),
    ]

    operations = [
        migrations.CreateModel(
            name='OPCR_Smart_kpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('opcr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opcr.opcr')),
                ('pillar_kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opcr.pillar_kpi')),
            ],
        ),
    ]
