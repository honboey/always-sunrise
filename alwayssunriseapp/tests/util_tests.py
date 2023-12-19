from datetime import datetime
import pytz

from django.test import TestCase
from ..utils.api_retrievals import get_lat_and_long, get_timezone, get_sunrise_times

class UtilTests(TestCase):
    # Test geocode API
    def test_get_lat_and_long__city_and_country(self):
        result = get_lat_and_long("Sydney, Australia")
        self.assertEqual(result, (-33.8688197, 151.2092955))

    def test_get_lat_and_long__city_only(self):
        result = get_lat_and_long("Sydney")
        self.assertEqual(result, (-33.8688197, 151.2092955))

    def test_get_lat_and_long__invalid_search(self):
        result = get_lat_and_long("als;dkfj")
        self.assertEqual(result, None)

    # Test timezone API
    def test_get_timezone(self):
        result = get_timezone((-33.8688197, 151.2092955))
        self.assertEqual(result, "Australia/Sydney")

    # Test sunrise API
    # def test_get_sunrise_times(self):
    #     result = get_sunrise_times("today", (-33.8688197, 151.2092955))
    #     print(result)
    #     self.assertEqual(
    #         result,
    #         datetime.datetime(
    #             2023, 12, 8, 5, 38, 36, tzinfo=pytz.timezone("Australia/Sydney")
    #         ),
    #     )
