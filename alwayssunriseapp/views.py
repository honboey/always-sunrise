from django.shortcuts import render, get_object_or_404
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
            return f"{minutes}min till sunrise"
        else:
            return f"{minutes}min after sunrise"
    else:
        time_str = f"{hours}h and {minutes}min"
        if is_positive:
            return f"{time_str} till sunrise"
        else:
            return f"{time_str} after sunrise"


def filter_future_sunrise_livestreams(livestream_queryset):
    """
    Queryset -> Queryset
    Given a queryset of livestream models remove all livestreams where the sunrise has already occurred.
    """
    future_sunrise_livestreams = livestream_queryset.filter(
        sunrise_time_today__gt=datetime.now(pytz.timezone("UTC"))
    )
    return future_sunrise_livestreams


def get_next_sunrise_livestream(livestream_queryset):
    """
    Queryset -> Livestream
    Given a queryset of livestreams, choose the livestream which is closest to its upcoming sunrise
    """
    # Get the current time in UTC
    current_time = timezone.now()

    # Calculate the time differences for each Livestream object
    time_differences = [
        (
            livestream,
            abs((current_time - livestream.sunrise_time_today).total_seconds()),
        )
        for livestream in livestream_queryset
    ]

    # Find the Livestream object with the shortest time difference
    nearest_livestream = min(time_differences, key=lambda x: x[1])[0]

    return nearest_livestream


# Create your views here.


def index(request):
    livestreams = Livestream.objects.all()
    current_time = datetime.now(pytz.utc)

    # Get correct livestream
    filtered_livestreams = filter_future_sunrise_livestreams(livestreams)
    upcoming_livestream = get_next_sunrise_livestream(filtered_livestreams)

    # Create string of time difference
    time_in_relation_to_sunrise = format_time_after_sunrise(
        upcoming_livestream.sunrise_time_today - current_time
    )
    return render(
        request,
        "alwayssunriseapp/index.html",
        {
            "livestream": upcoming_livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
        },
    )


def livestream_list(request):
    livestreams = Livestream.objects.all()
    current_time = datetime.now(pytz.utc)

    return render(
        request,
        "alwayssunriseapp/livestream_list.html",
        {
            "livestreams": livestreams,
            "current_time": current_time,
        },
    )


def single_livestream(request, pk):
    livestream = get_object_or_404(Livestream, pk=pk)
    current_time = datetime.now(pytz.utc)

    time_in_relation_to_sunrise = format_time_after_sunrise(
        livestream.sunrise_time_today - current_time
    )

    return render(
        request,
        "alwayssunriseapp/single_livestream.html",
        {
            "livestream": livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
        },
    )
