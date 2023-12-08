import factory
from datetime import datetime, timedelta
import pytz

from .models import Livestream


class LivestreamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Livestream

    location = factory.Faker("city")
    youtube_id = factory.Faker("bothify", text="??????????")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    timezone = factory.Faker("timezone")
    sunrise_time_today = factory.LazyFunction(
        lambda: datetime.now(pytz.timezone("UTC")) + timedelta(hours=1)
    )
    sunrise_time_tomorrow = factory.LazyFunction(
        lambda: datetime.now(pytz.timezone("UTC")) + timedelta(days=1, hours=1)
    )
    weather = factory.Faker("word")
