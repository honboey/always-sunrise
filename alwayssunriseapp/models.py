from django.conf import settings
from django.db import models
from datetime import datetime, timedelta


class Livestream(models.Model):
    location = models.CharField(max_length=200)
    livestream_url = models.URLField()
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    timezone = models.CharField(max_length=200)
    sunrise_time_today = models.DateTimeField()
    sunrise_time_tomorrow = models.DateTimeField()
    weather = models.CharField(max_length=200)

    def __str__(self):
        return self.location
