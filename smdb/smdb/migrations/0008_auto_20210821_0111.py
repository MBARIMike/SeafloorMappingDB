# Generated by Django 3.2.6 on 2021-08-21 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smdb', '0007_rename_platform_type_name_platformtype_platformtype_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, unique=True)),
                ('value', models.CharField(max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='missiontype',
            name='missiontype_name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='sensor_type_name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
