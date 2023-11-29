import requests
import pytz

from django.core.management.base import BaseCommand
from alwayssunriseapp.models import Livestream
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Testing a command"

    def handle(self, *args, **options):
        livestreams = Livestream.objects.all()

        for livestream in livestreams:
            # Today's sunrise information

            sunrise_response_today = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}&date=today"
            )
            if sunrise_response_today.status_code == 200:
                # Convert received time to naive datetime.time object
                sunrise_time_today = datetime.strptime(
                    sunrise_response_today.json()["results"]["sunrise"], "%I:%M:%S %p"
                ).time()

                # Get timezone and convert to pytz.timezone object
                local_timezone = pytz.timezone(
                    sunrise_response_today.json()["results"]["timezone"]
                )

                # Get today's date and convert to datetime.date
                today_date = datetime.now().date()

                # Combine time and date to create a naive datetime.datetime object
                naive_local_sunrise_time_today = datetime.combine(
                    today_date, sunrise_time_today
                )

                # Save naive datetime.datetime object to model
                livestream.local_sunrise_time_today = naive_local_sunrise_time_today


                # Add timezone to model
                livestream.timezone = sunrise_response_today.json()["results"][
                    "timezone"
                ]

                print(livestream.location, livestream.local_sunrise_time_today, livestream.local_sunrise_time_today.tzinfo)

            # Tomorrow's sunrise information

            sunrise_response_tomorrow = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}&date=tomorrow"
            )
            if sunrise_response_tomorrow.status_code == 200:
                # Convert received time to datetime.time object
                sunrise_time_tomorrow = datetime.strptime(
                    sunrise_response_tomorrow.json()["results"]["sunrise"],
                    "%I:%M:%S %p",
                ).time()

                # Get tomorrow's date
                tomorrow_date = datetime.now().date() + timedelta(days=1)

                # Get timezone
                local_timezone = pytz.timezone(
                    sunrise_response_tomorrow.json()["results"]["timezone"]
                )
                # print("\n\n\n\n\n\n", local_timezone, type(local_timezone), "\n\n\n")

                # Combine the two to create a datetime.datetime object
                livestream.local_sunrise_time_tomorrow = datetime.combine(
                    tomorrow_date, sunrise_time_tomorrow
                ).replace(tzinfo=local_timezone)

            livestream.save()
