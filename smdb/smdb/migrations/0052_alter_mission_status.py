# Generated by Django 4.2.9 on 2024-05-16 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("smdb", "0051_alter_mission_start_depth_alter_mission_track_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PS", "production_survey"),
                    ("FS", "failed_survey"),
                    ("TS", "test_survey"),
                    ("RS", "repeat_survey"),
                    ("DNU", "do_not_use_survey"),
                    ("UWC", "use_with_caution"),
                ],
                max_length=128,
                null=True,
            ),
        ),
    ]
