# Generated by Django 4.1.5 on 2023-01-21 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_remove_vehiclestation_vehicle_vehicle_station'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclehistory',
            name='vehicle_station',
        ),
        migrations.AlterField(
            model_name='vehiclehistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]