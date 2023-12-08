import pytz
from datetime import datetime, timedelta
from freezegun import freeze_time

from django.test import TestCase
from django.utils import timezone

from ..models import Livestream
from ..factories import LivestreamFactory
from ..views import filter_future_sunrise_livestreams, get_next_sunrise_livestream

# Create your tests here.


class IndexViewTests(TestCase):
    def setUp(self):
        # Setup Livestream objects
        self.sydney = LivestreamFactory(
            location = "Sydney",
            sunrise_time_today = datetime(
                2023, 12, 7, 5, 30, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
            sunrise_time_tomorrow = datetime(
                2023, 12, 8, 5, 31, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
        )

        self.tokyo = LivestreamFactory(
            location = "Tokyo",
            sunrise_time_today = datetime(
                2023, 12, 7, 6, 30, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            ),
            sunrise_time_tomorrow = datetime(
                2023, 12, 8, 6, 31, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            )
        )
        

    @freeze_time("2023-12-6 17:15:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_before_all_today_sunrise(self):
        filtered_livestreams = filter_future_sunrise_livestreams(Livestream.objects.all())
        self.assertQuerysetEqual(filtered_livestreams, [self.tokyo, self.sydney])


    @freeze_time("2023-12-7 20:00:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_between_sydney_and_tokyo_tomorrow_sunrise(self):
        filtered_livestreams = filter_future_sunrise_livestreams(Livestream.objects.all())
        self.assertQuerysetEqual(filtered_livestreams, [self.tokyo])


    @freeze_time("2023-12-8 20:00:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_after_sydney_and_tokyo_tomorrow_sunrise(self):
        filtered_livestreams = filter_future_sunrise_livestreams(Livestream.objects.all())
        self.assertQuerysetEqual(filtered_livestreams, [])


    # @freeze_time("2023-12-3 19:30:00", tz_offset=0)
    # def test_get_next_sunrise_livestream(self):
    #     # Livestream setup
    #     sydney_timezone = "Australia/Sydney"
    #     sydney_sunrise_time_today = datetime(
    #         2023, 12, 4, 5, 30, 0, tzinfo=pytz.timezone(sydney_timezone)
    #     )
    #     sydney_sunrise_time_tomorrow = datetime(
    #         2023, 12, 5, 5, 31, 0, tzinfo=pytz.timezone(sydney_timezone)
    #     )

    #     sydney = create_livestream(
    #         "Sydney",
    #         sydney_sunrise_time_today,
    #         sydney_sunrise_time_tomorrow,
    #         sydney_timezone,
    #     )

    #     tokyo_timezone = "Asia/Tokyo"
    #     tokyo_sunrise_time_today = datetime(
    #         2023, 12, 4, 6, 24, 0, tzinfo=pytz.timezone(tokyo_timezone)
    #     )
    #     tokyo_sunrise_time_tomorrow = datetime(
    #         2023, 12, 5, 6, 25, 0, tzinfo=pytz.timezone(tokyo_timezone)
    #     )

    #     tokyo = create_livestream(
    #         "Tokyo",
    #         tokyo_sunrise_time_today,
    #         tokyo_sunrise_time_tomorrow,
    #         tokyo_timezone,
    #     )

    #     nyc_timezone = "America/New_York"
    #     nyc_sunrise_time_today = datetime(
    #         2023, 12, 4, 5, 39, 0, tzinfo=pytz.timezone(nyc_timezone)
    #     )
    #     nyc_sunrise_time_tomorrow = datetime(
    #         2023, 12, 5, 5, 40, 0, tzinfo=pytz.timezone(nyc_timezone)
    #     )

    #     nyc = create_livestream(
    #         "New York",
    #         nyc_sunrise_time_today,
    #         nyc_sunrise_time_tomorrow,
    #         nyc_timezone,
    #     )

    #     livestreams = Livestream.objects.all()
    #     filtered_livestreams = filter_future_sunrise_livestreams(livestreams)
    #     upcoming_livestream = get_next_sunrise_livestream(filtered_livestreams)

    #     self.assertEqual(upcoming_livestream, tokyo)
