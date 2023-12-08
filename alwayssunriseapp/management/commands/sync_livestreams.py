import requests
import pytz
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from alwayssunriseapp.models import Livestream
from alwayssunriseapp.utils.api_retrievals import get_sunrise_times


class Command(BaseCommand):
    help = "Call sunrise API and get sunrise times for Livestream"

    def handle(self, *args, **options):
        livestreams = Livestream.objects.all()

        for livestream in livestreams:
            livestream.sunrise_time_today = get_sunrise_times(
                "today",
                (livestream.latitude, livestream.longitude),
            )
            livestream.sunrise_time_tomorrow = get_sunrise_times(
                "tomorrow",
                (livestream.latitude, livestream.longitude),
            )

            livestream.save()
            print(
                livestream, livestream.sunrise_time_today, livestream.timezone, "today"
            )
            print(
                livestream,
                livestream.sunrise_time_tomorrow,
                livestream.timezone,
                "tomorrow",
            )
