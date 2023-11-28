from django.conf import settings
from django.db import models
from django.utils import timezone


class Livestream(models.Model):
	location = models.CharField(max_length=200)
	livestream_url = models.URLField() 
	local_sunrise_time = models.TimeField()
	local_time = models.TimeField()
	weather = models.CharField(max_length=200)

	def __str__(self):
		return self.location
