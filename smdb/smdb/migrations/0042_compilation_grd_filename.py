# Generated by Django 3.2.11 on 2022-02-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smdb', '0041_compilation_cmd_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='compilation',
            name='grd_filename',
            field=models.FileField(blank=True, max_length=128, null=True, upload_to=''),
        ),
    ]
