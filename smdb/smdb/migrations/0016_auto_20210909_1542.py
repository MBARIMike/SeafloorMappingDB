# Generated by Django 3.2.6 on 2021-09-09 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smdb', '0015_alter_mission_kml_filename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='platform_type',
            new_name='platformtype',
        ),
        migrations.RenameField(
            model_name='sensor',
            old_name='sensor_type',
            new_name='sensortype',
        ),
    ]