from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
from .utils.api_retrievals import get_lat_and_long

# Create object


class Livestream(models.Model):
    location = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    timezone = models.CharField(max_length=200)
    sunrise_time_today = models.DateTimeField()
    sunrise_time_tomorrow = models.DateTimeField()
    weather = models.CharField(max_length=200)

    def __str__(self):
        return self.location
    
    def save(self, *args, **kwargs):
        print(get_lat_and_long(self.location))
        # Call Geocode API to get lat and long of location
        try:
            self.latitude, self.longitude = get_lat_and_long(self.location)
        except:
            self.latitude = 0.0
            self.longitude = 0.0
        
        super().save(*args, **kwargs)
