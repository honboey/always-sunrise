import requests

from django.core.management.base import BaseCommand
from alwayssunriseapp.models import Livestream
from datetime import datetime


class Command(BaseCommand):
    help = "Testing a command"

    def handle(self, *args, **options):
        livestreams = Livestream.objects.all()

        for livestream in livestreams:
            sunrise_response = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}"
            )

            sunrise = datetime.strptime(
                sunrise_response.json()["results"]["sunrise"], "%I:%M:%S %p"
            ).time()

            if sunrise_response.status_code == 200:
                livestream.local_sunrise_time = sunrise
                livestream.save()
