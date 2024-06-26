# Generated by Django 4.2.9 on 2024-05-21 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("smdb", "0052_alter_mission_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mission",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("production_survey", "production_survey"),
                    ("failed_survey", "failed_survey"),
                    ("test_survey", "test_survey"),
                    ("repeat_survey", "repeat_survey"),
                    ("do_not_use_survey", "do_not_use_survey"),
                    ("use_with_caution", "use_with_caution"),
                ],
                max_length=128,
                null=True,
            ),
        ),
    ]
