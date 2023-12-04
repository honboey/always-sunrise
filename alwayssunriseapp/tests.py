from django.test import TestCase
from django.utils import timezone
from .models import Livestream
from .views import filter_future_sunrise_livestreams, get_next_sunrise_livestream
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
    @freeze_time("2023-12-3 19:30:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams(self):
        """
        Given a list of livestreams, remove all livestreams where the sunrise has occurred
        """

        # Livestream setup
        sydney_timezone = "Australia/Sydney"
        sydney_sunrise_time_today = datetime(
            2023, 12, 4, 5, 30, 0, tzinfo=pytz.timezone(sydney_timezone)
        )
        sydney_sunrise_time_tomorrow = datetime(
            2023, 12, 5, 5, 31, 0, tzinfo=pytz.timezone(sydney_timezone)
        )

        sydney = create_livestream(
            "Sydney",
            sydney_sunrise_time_today,
            sydney_sunrise_time_tomorrow,
            sydney_timezone,
        )

        tokyo_timezone = "Asia/Tokyo"
        tokyo_sunrise_time_today = datetime(
            2023, 12, 4, 6, 24, 0, tzinfo=pytz.timezone(tokyo_timezone)
        )
        tokyo_sunrise_time_tomorrow = datetime(
            2023, 12, 5, 6, 25, 0, tzinfo=pytz.timezone(tokyo_timezone)
        )

        tokyo = create_livestream(
            "Tokyo",
            tokyo_sunrise_time_today,
            tokyo_sunrise_time_tomorrow,
            tokyo_timezone,
        )

        livestreams = Livestream.objects.all()
        filtered_livestreams = filter_future_sunrise_livestreams(livestreams)

        self.assertQuerysetEqual(filtered_livestreams, [tokyo])

    @freeze_time("2023-12-3 19:30:00", tz_offset=0)
    def test_get_next_sunrise_livestream(self):
        # Livestream setup
        sydney_timezone = "Australia/Sydney"
        sydney_sunrise_time_today = datetime(
            2023, 12, 4, 5, 30, 0, tzinfo=pytz.timezone(sydney_timezone)
        )
        sydney_sunrise_time_tomorrow = datetime(
            2023, 12, 5, 5, 31, 0, tzinfo=pytz.timezone(sydney_timezone)
        )

        sydney = create_livestream(
            "Sydney",
            sydney_sunrise_time_today,
            sydney_sunrise_time_tomorrow,
            sydney_timezone,
        )

        tokyo_timezone = "Asia/Tokyo"
        tokyo_sunrise_time_today = datetime(
            2023, 12, 4, 6, 24, 0, tzinfo=pytz.timezone(tokyo_timezone)
        )
        tokyo_sunrise_time_tomorrow = datetime(
            2023, 12, 5, 6, 25, 0, tzinfo=pytz.timezone(tokyo_timezone)
        )

        tokyo = create_livestream(
            "Tokyo",
            tokyo_sunrise_time_today,
            tokyo_sunrise_time_tomorrow,
            tokyo_timezone,
        )

        nyc_timezone = "America/New_York"
        nyc_sunrise_time_today = datetime(
            2023, 12, 4, 5, 39, 0, tzinfo=pytz.timezone(nyc_timezone)
        )
        nyc_sunrise_time_tomorrow = datetime(
            2023, 12, 5, 5, 40, 0, tzinfo=pytz.timezone(nyc_timezone)
        )

        nyc = create_livestream(
            "New York",
            nyc_sunrise_time_today,
            nyc_sunrise_time_tomorrow,
            nyc_timezone,
        )

        livestreams = Livestream.objects.all()
        filtered_livestreams = filter_future_sunrise_livestreams(livestreams)
        upcoming_livestream = get_next_sunrise_livestream(filtered_livestreams)

        self.assertEqual(upcoming_livestream, tokyo)
