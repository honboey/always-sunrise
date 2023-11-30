from django.shortcuts import render
from django.utils import timezone
from .models import Livestream
from datetime import datetime, timedelta

import pytz

# Common utility functions


# Create string of time difference
def format_time_after_sunrise(timedelta_object):
    """
    Given a timedelta object of the difference of time between
    the current time and the sunrise, render that difference as a string.
    """
    # Extract hours and minutes from timedelta
    hours, minutes = divmod(timedelta_object.seconds // 60, 60)

    # Determine if it's positive or negative
    is_positive = timedelta_object.total_seconds() >= 0

    # Build the string based on the conditions
    if hours == 0 and minutes < 60:
        if is_positive:
            return f"{minutes}min after sunrise"
        else:
            return f"{minutes}min till sunrise"
    else:
        time_str = f"{hours}h and {minutes}min"
        if is_positive:
            return f"{time_str} after sunrise"
        else:
            return f"{time_str} till sunrise"


def display_appropriate_livestream(livestream_queryset):
    """
    Queryset -> Livestream model
    Given a queryset of livestream models, choose the one which is closest to its
    upcoming sunrise time.
    The conditions are:
    • Sunrise must be in the future
    • It's time to sunrise must be the smallest out of all in the queryset
    """
    for livestream in livestream_queryset:
        current_time = datetime.now(pytz.timezone(livestream.timezone))
        if livestream.sunrise_time_today > current_time:
            print(f"{livestream} will be deleted")
            


# Create your views here.


def index(request):
    livestream = Livestream.objects.get(location__contains="Tokyo")
    current_time = datetime.now(pytz.timezone(livestream.timezone))
    time_difference = current_time - livestream.sunrise_time_today

    # Create string of time difference
    time_in_relation_to_sunrise = format_time_after_sunrise(time_difference)

    return render(
        request,
        "alwayssunriseapp/index.html",
        {
            "livestream": livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
        },
    )


def livestream_list(request):
    livestreams = Livestream.objects.filter(
        sunrise_time_today__lte=timezone.now()
    ).order_by("sunrise_time_today")

    return render(
        request, "alwayssunriseapp/livestream_list.html", {"livestreams": livestreams}
    )
