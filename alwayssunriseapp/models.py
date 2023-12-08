from django.conf import settings
from django.db import models
from datetime import datetime, timedelta

from .utils.api_retrievals import get_lat_and_long, get_sunrise_times, get_timezone

# Create object


class Livestream(models.Model):
    location = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20, null=True)
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    timezone = models.CharField(max_length=200, null=True, blank=True)
    sunrise_time_today = models.DateTimeField(blank=True)
    sunrise_time_tomorrow = models.DateTimeField(blank=True)
    weather = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ["timezone"]

    def __str__(self):
        return self.location

    def save(self, *args, **kwargs):
        # Call Geocode API to get lat and long of location
        try:
            self.latitude, self.longitude = get_lat_and_long(self.location)
        except:
            self.latitude = 0.0
            self.longitude = 0.0

        # Call Timezone API
        try:
            self.timezone = get_timezone((self.latitude, self.longitude))
        except:
            self.timezone = "UTC"

        # Call sunrise API
        self.sunrise_time_today = get_sunrise_times(
            "today", (self.latitude, self.longitude)
        )
        self.sunrise_time_tomorrow = get_sunrise_times(
            "tomorrow", (self.latitude, self.longitude)
        )

        super().save(*args, **kwargs)
