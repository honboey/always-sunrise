# Generated by Django 4.2.7 on 2023-11-29 03:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alwayssunriseapp", "0003_remove_livestream_local_sunrise_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="livestream",
            name="utc_sunrise_time_today",
            field=models.TimeField(default="06:56:44"),
        ),
        migrations.AddField(
            model_name="livestream",
            name="utc_sunrise_time_tomorrow",
            field=models.TimeField(default="06:56:44"),
        ),
    ]
