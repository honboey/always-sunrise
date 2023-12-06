from django.test import TestCase
from django.utils import timezone
from ..models import Livestream
from ..utils.api_retrievals import get_lat_and_long
import pytz
from datetime import datetime, timedelta
from freezegun import freeze_time


class UtilTests(TestCase):
    def test_get_lat_and_long__city_and_country(self):
        result = get_lat_and_long("Sydney, Australia")
        self.assertEqual(result, (-33.8688197, 151.2092955))

    def test_get_lat_and_long__city_only(self):
        result = get_lat_and_long("Sydney")
        self.assertEqual(result, (-33.8688197, 151.2092955))

    def test_get_lat_and_long__invalid_search(self):
        result = get_lat_and_long("als;dkfj")
        self.assertEqual(result, None)