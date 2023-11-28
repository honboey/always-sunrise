from django.conf import settings
from django.db import models
from django.utils import timezone


class Livestream(models.Model):
    location = models.CharField(max_length=200)
    livestream_url = models.URLField()
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=-33.867778)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=151.21)
    local_sunrise_time = models.TimeField()
    local_time = models.TimeField()
    weather = models.CharField(max_length=200)

    def __str__(self):
        return self.location
