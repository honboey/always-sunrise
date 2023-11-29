import requests

from django.core.management.base import BaseCommand
from alwayssunriseapp.models import Livestream
from datetime import datetime


class Command(BaseCommand):
    help = "Testing a command"

    def handle(self, *args, **options):
        livestreams = Livestream.objects.all()

        for livestream in livestreams:
            sunrise_response_today = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}&date=today"
            )
            if sunrise_response_today.status_code == 200:
                sunrise_time_today = datetime.strptime(
                    sunrise_response_today.json()["results"]["sunrise"], "%I:%M:%S %p"
                ).time()
                livestream.local_sunrise_time_today = sunrise_time_today

            sunrise_response_tomorrow = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}&date=tomorrow"
            )
            if sunrise_response_tomorrow.status_code == 200:
                sunrise_time_tomorrow = datetime.strptime(
                    sunrise_response_tomorrow.json()["results"]["sunrise"], "%I:%M:%S %p"
                ).time()
                livestream.local_sunrise_time_tomorrow = sunrise_time_tomorrow

            livestream.save()
