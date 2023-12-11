import pytz
from datetime import datetime, timedelta
from freezegun import freeze_time

from django.test import TestCase
from django.utils import timezone

from ..models import Livestream
from ..factories import LivestreamFactory
from ..views import (
    filter_future_sunrise_livestreams,
    get_next_sunrise_livestream,
    get_sunrise_time_relationship,
    sort_livestreams_by_time,
)

# Create your tests here.


class IndexViewTests(TestCase):
    def setUp(self):
        # Setup Livestream objects
        self.sydney = LivestreamFactory(
            location="Sydney",
            sunrise_time_today=datetime(
                2023, 12, 7, 5, 30, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 5, 31, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
        )

        self.tokyo = LivestreamFactory(
            location="Tokyo",
            sunrise_time_today=datetime(
                2023, 12, 7, 6, 30, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 6, 31, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            ),
        )

        self.nyc = LivestreamFactory(
            location="NYC",
            sunrise_time_today=datetime(
                2023, 12, 7, 7, 7, 0, tzinfo=pytz.timezone("America/New_York")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 7, 8, 0, tzinfo=pytz.timezone("America/New_York")
            ),
        )

    # filter_future_sunrise_livestreams()
    @freeze_time("2023-12-6 17:15:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_before_all_today_sunrise(
        self,
    ):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        self.assertQuerysetEqual(
            filtered_livestreams, [self.nyc, self.tokyo, self.sydney]
        )

    @freeze_time("2023-12-7 20:00:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_between_sydney_and_tokyo_tomorrow_sunrise(
        self,
    ):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        self.assertQuerysetEqual(filtered_livestreams, [self.nyc, self.tokyo])

    @freeze_time("2023-12-8 20:00:00", tz_offset=0)
    def test_filter_future_sunrise_livestreams__current_time_after_sydney_and_tokyo_tomorrow_sunrise(
        self,
    ):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        self.assertQuerysetEqual(filtered_livestreams, [])

    # get_next_sunrise_livestream()
    @freeze_time("2023-12-6 17:15:00", tz_offset=0)
    def test_get_next_sunrise_livestream__current_time_is_before_sydney_today(self):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        livestream = get_next_sunrise_livestream(filtered_livestreams)
        self.assertEqual(livestream, self.sydney)

    @freeze_time("2023-12-7 12:59:00", tz_offset=0)
    def test_get_next_sunrise_livestream__current_time_is_between_nyc_today_and_sydney_tomorrow(
        self,
    ):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        livestream = get_next_sunrise_livestream(filtered_livestreams)
        self.assertEqual(livestream, self.sydney)

    @freeze_time("2023-12-7 12:00:00", tz_offset=0)
    def test_get_next_sunrise_livestream__current_time_is_before_nyc_today(
        self,
    ):
        filtered_livestreams = filter_future_sunrise_livestreams(
            Livestream.objects.all()
        )
        livestream = get_next_sunrise_livestream(filtered_livestreams)
        self.assertEqual(livestream, self.nyc)

    # get_sunrise_time_relationship()
    @freeze_time("2023-12-6 16:00:00", tz_offset=0)
    def test_get_sunrise_time_relationship__current_time_before_sunrise_today(self):
        statement = get_sunrise_time_relationship(self.tokyo)
        self.assertEqual(statement, "5h 11mins till sunrise")

    @freeze_time("2023-12-6 21:00:00", tz_offset=0)
    def test_get_sunrise_time_relationship__current_time_less_than_an_hour_before_sunrise_today(
        self,
    ):
        statement = get_sunrise_time_relationship(self.tokyo)
        self.assertEqual(statement, "11mins till sunrise")

    @freeze_time("2023-12-8 02:00:00", tz_offset=0)
    def test_get_sunrise_time_relationship__current_time_after_sunrise_tomorrow(self):
        statement = get_sunrise_time_relationship(self.tokyo)
        self.assertEqual(statement, "4h 48mins after sunrise")

    @freeze_time("2023-12-6 23:00:00", tz_offset=0)
    def test_get_sunrise_time_relationship__current_time_just_after_sunrise_today(self):
        statement = get_sunrise_time_relationship(self.tokyo)
        self.assertEqual(statement, "1h 49mins after sunrise")

    @freeze_time("2023-12-7 20:00:00", tz_offset=0)
    def test_get_sunrise_time_relationship__current_time_just_before_sunrise_tomorrow(
        self,
    ):
        statement = get_sunrise_time_relationship(self.tokyo)
        self.assertEqual(statement, "1h 12mins till sunrise")


class ViewSortingTests(TestCase):
    def setUp(self):
        # Setup Livestream objects
        self.sydney = LivestreamFactory(
            location="Sydney",
            sunrise_time_today=datetime(
                2023, 12, 7, 5, 30, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 5, 31, 0, tzinfo=pytz.timezone("Australia/Sydney")
            ),
        )

        self.tokyo = LivestreamFactory(
            location="Tokyo",
            sunrise_time_today=datetime(
                2023, 12, 7, 6, 30, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 6, 31, 0, tzinfo=pytz.timezone("Asia/Tokyo")
            ),
        )

        self.nyc = LivestreamFactory(
            location="NYC",
            sunrise_time_today=datetime(
                2023, 12, 7, 7, 7, 0, tzinfo=pytz.timezone("America/New_York")
            ),
            sunrise_time_tomorrow=datetime(
                2023, 12, 8, 7, 8, 0, tzinfo=pytz.timezone("America/New_York")
            ),
        )

    def test_sort_livestreams_by_time(self):
        sorted_livestreams = sort_livestreams_by_time(Livestream.objects.all())
        # self.assertQuerySetEqual([self.nyc, self.sydney, self.tokyo], sorted_livestreams)
