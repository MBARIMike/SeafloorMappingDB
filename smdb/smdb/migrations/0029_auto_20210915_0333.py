# Generated by Django 3.2.7 on 2021-09-15 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smdb', '0028_alter_mission_thumbnail_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='thumbnail_url',
        ),
        migrations.AlterField(
            model_name='mission',
            name='thumbnail_image',
            field=models.ImageField(blank=True, upload_to='thumbnails'),
        ),
    ]