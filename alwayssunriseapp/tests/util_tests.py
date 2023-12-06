from django.test import TestCase
from django.utils import timezone
from ..models import Livestream
from ..utils.api_retrievals import get_lat_and_long
import pytz
from datetime import datetime, timedelta
from freezegun import freeze_time


class UtilTests(TestCase):
    def test_get_lat_and_long(self):
        get_lat_and_long("Sydney, Australia")
