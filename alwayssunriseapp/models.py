import pytz

from django.conf import settings
from django.db import models
from datetime import datetime, timedelta


class Livestream(models.Model):
    location = models.CharField(max_length=200)
    livestream_url = models.URLField()
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=-33.867778)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=151.21)
    timezone = models.CharField(max_length=200)
    local_sunrise_time_today = models.DateTimeField()
    utc_sunrise_time_today = models.DateTimeField()
    local_sunrise_time_tomorrow = models.DateTimeField()
    utc_sunrise_time_tomorrow = models.DateTimeField()
    local_time = models.DateTimeField()
    weather = models.CharField(max_length=200)

    def __str__(self):
        return self.location

    # def save(self, *args, **kwargs):
    #     local_timezone = pytz.timezone(self.timezone)
    #     target_timezone = pytz.UTC
    #     utc_datetime = self.local_sunrise_time_today.astimezone()

    # print(type(self.local_sunrise_time_today))
