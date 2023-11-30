from django.test import TestCase
from django.utils import timezone
from .models import Livestream
from .views import display_appropriate_livestream
import pytz
from datetime import datetime, timedelta
from freezegun import freeze_time

# Create your tests here.


def create_livestream(location, sunrise_time_today, sunrise_time_tomorrow, timezone):
	return Livestream.objects.create(
		location=location,
		sunrise_time_today=sunrise_time_today,
		sunrise_time_tomorrow=sunrise_time_tomorrow,
		timezone=timezone,
		latitude=12.1234,
		longitude=12.1234,
	)


class IndexViewTests(TestCase):
	@freeze_time("2023-01-15 05:30:00")
	def test_choose_correct_livestream(self):
		"""
		Given a list of livestreams, choose the best one to display
		"""

		# Livestream setup
		sydney_timezone = "Australia/Sydney"
		sydney_sunrise_time_today = datetime(
			2023, 11, 30, 6, 30, 0, tzinfo=pytz.timezone(sydney_timezone)
		)
		sydney_sunrise_time_tomorrow = datetime(
			2023, 12, 1, 6, 31, 0, tzinfo=pytz.timezone(sydney_timezone)
		)

		create_livestream(
			"Sydney",
			sydney_sunrise_time_today,
			sydney_sunrise_time_tomorrow,
			sydney_timezone,
		)

		tokyo_timezone = "Asia/Tokyo"
		tokyo_sunrise_time_today = datetime(
			2023, 11, 30, 5, 24, 0, tzinfo=pytz.timezone(tokyo_timezone)
		)
		tokyo_sunrise_time_tomorrow = datetime(
			2023, 12, 1, 5, 25, 0, tzinfo=pytz.timezone(tokyo_timezone)
		)

		create_livestream(
			"Tokyo",
			tokyo_sunrise_time_today,
			tokyo_sunrise_time_tomorrow,
			tokyo_timezone,
		)

		livestreams = Livestream.objects.all()
		display_appropriate_livestream(livestreams)
