from django.test import TestCase
from ..utils.api_retrievals import get_lat_and_long


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