# Generated by Django 5.1.2 on 2024-10-29 00:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opcr', '0005_alter_activitiesopcr_employee'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitiesdpcr',
            old_name='waitallocation',
            new_name='weightallocation',
        ),
        migrations.RenameField(
            model_name='activitiesopcr',
            old_name='waitallocation',
            new_name='weightallocation',
        ),
        migrations.AlterField(
            model_name='activitiesdpcr',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ActivitiesDPCR', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ipcr_opcr',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
