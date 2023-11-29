import requests
import pytz

from django.core.management.base import BaseCommand
from alwayssunriseapp.models import Livestream
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Call sunrise API and get sunrise times for Livestream"

    def handle(self, *args, **options):
        livestreams = Livestream.objects.all()

        def get_sunrise_time(day, livestream):
            """
            Given a day and Livestream model, update the Livestream model with the sunrise time for that day
            """
            response = requests.get(
                f"https://api.sunrisesunset.io/json?lat={livestream.latitude}&lng={livestream.longitude}&date={day}"
            )
            if response.status_code == 200:
                # Convert received time to naive datetime.time object
                sunrise_time = datetime.strptime(
                    response.json()["results"]["sunrise"], "%I:%M:%S %p"
                ).time()

                # Get timezone and convert to pytz.timezone object
                local_timezone = pytz.timezone(response.json()["results"]["timezone"])

                # Get day's date and convert to datetime.date
                if day == "today":
                    date = datetime.now().date()
                elif day == "tomorrow":
                    date = datetime.now().date() + timedelta(days=1)

                # Combine time and date to create a naive datetime.datetime object
                naive_sunrise_datetime = datetime.combine(date, sunrise_time)

                # Convert to aware datetime.datetime object and save to model
                if day == "today":
                    livestream.sunrise_time_today = local_timezone.localize(
                        naive_sunrise_datetime
                    )
                elif day == "tomorrow":
                    livestream.sunrise_time_tomorrow = local_timezone.localize(
                        naive_sunrise_datetime
                    )

                # Add timezone to model
                livestream.timezone = response.json()["results"]["timezone"]

                livestream.save()
                print(livestream, sunrise_time, day, livestream.timezone)

        for livestream in livestreams:
            get_sunrise_time("today", livestream)
            get_sunrise_time("tomorrow", livestream)
