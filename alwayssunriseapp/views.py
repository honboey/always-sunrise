from django.shortcuts import render, get_object_or_404
from .models import Livestream
from datetime import datetime, timedelta

import pytz

# Common utility functions


# Create string of time difference
def get_sunrise_time_relationship(livestream):
    """
    Given a livestream object of the difference of time between
    the current time and the sunrise, render that difference as a string.
    """
    current_time = datetime.now(pytz.timezone("UTC"))

    def convert_timedelta_to_human_readable_string(timedelta):
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return (hours, minutes)

    if livestream.sunrise_time_today > current_time:
        time_diff = livestream.sunrise_time_today - current_time
        time_diff_str = convert_timedelta_to_human_readable_string(time_diff)
        if time_diff_str[0] == 0:
            return f"{time_diff_str[1]}mins till sunrise"
        else:
            return f"{time_diff_str[0]}h {time_diff_str[1]}mins till sunrise"

    elif livestream.sunrise_time_tomorrow < current_time:
        time_diff = current_time - livestream.sunrise_time_tomorrow
        time_diff_str = convert_timedelta_to_human_readable_string(time_diff)
        if time_diff_str[0] == 0:
            return f"{time_diff_str[1]}mins after sunrise"
        else:
            return f"{time_diff_str[0]}h {time_diff_str[1]}mins after sunrise"

    else:
        time_diff_from_sunrise_today = livestream.sunrise_time_tomorrow - current_time
        if int(time_diff_from_sunrise_today.total_seconds()) > 21600:
            time_diff = current_time - livestream.sunrise_time_today
            time_diff_str = convert_timedelta_to_human_readable_string(time_diff)
            if time_diff_str[0] == 0:
                return f"{time_diff_str[1]}mins after sunrise"
            else:
                return f"{time_diff_str[0]}h {time_diff_str[1]}mins after sunrise"
        else:
            time_diff = livestream.sunrise_time_tomorrow - current_time
            time_diff_str = convert_timedelta_to_human_readable_string(time_diff)
            if time_diff_str[0] == 0:
                return f"{time_diff_str[1]}mins till sunrise"
            else:
                return f"{time_diff_str[0]}h {time_diff_str[1]}mins till sunrise"


def filter_future_sunrise_livestreams(livestream_queryset):
    """
    Queryset -> Queryset
    Given a queryset of livestream models remove all livestreams where the sunrise has already occurred.
    """
    future_sunrise_livestreams = livestream_queryset.filter(
        sunrise_time_tomorrow__gt=datetime.now(pytz.timezone("UTC"))
    )
    return future_sunrise_livestreams


def get_next_sunrise_livestream(livestream_queryset):
    """
    Queryset -> Livestream
    Given a queryset of livestreams, choose the livestream which is closest to its upcoming sunrise
    """
    # Get the current time in UTC
    current_time = datetime.now(pytz.timezone("UTC"))
    time_differences = []
    """
    This will look like:
    [
        {
            "livestream": livestream, 
            "time_to_next_sunrise": 123
        },
        {
            "livestream": livestream, 
            "time_to_next_sunrise": 123
        },
    ]
    """
    for livestream in livestream_queryset:
        if livestream.sunrise_time_today > current_time:
            time_to_next_sunrise = livestream.sunrise_time_today - current_time
        else:
            time_to_next_sunrise = livestream.sunrise_time_tomorrow - current_time

        time_differences.append(
            {
                "livestream": livestream,
                "time_to_next_sunrise": int(time_to_next_sunrise.total_seconds()),
            }
        )

    selected_livestream = min(
        time_differences,
        key=lambda time_to_next_sunrise: time_to_next_sunrise["time_to_next_sunrise"],
    )["livestream"]
    return selected_livestream


# Create your views here.


def index(request):
    livestreams = Livestream.objects.all()
    current_time = datetime.now(pytz.utc)

    # Get correct livestream
    filtered_livestreams = filter_future_sunrise_livestreams(livestreams)
    upcoming_livestream = get_next_sunrise_livestream(filtered_livestreams)

    # Create string of time difference
    time_in_relation_to_sunrise = get_sunrise_time_relationship(upcoming_livestream)
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
    livestreams = Livestream.objects.all().order_by("sunrise_time_today")
    current_time = datetime.now(pytz.utc)
    filtered_livestreams = filter_future_sunrise_livestreams(livestreams)
    current_livestream = get_next_sunrise_livestream(filtered_livestreams)
    livestream_additional_info = []

    for livestream in livestreams:
        if livestream == current_livestream:
            livestream_additional_info.append(
                {
                    "livestream": livestream,
                    "time_in_relation_to_sunrise": get_sunrise_time_relationship(
                        livestream
                    ),
                    "current_livestream": True,
                }
            )
        else:
            livestream_additional_info.append(
                {
                    "livestream": livestream,
                    "time_in_relation_to_sunrise": get_sunrise_time_relationship(
                        livestream
                    ),
                }
            )

    print(livestream_additional_info)

    return render(
        request,
        "alwayssunriseapp/livestream_list.html",
        {
            "livestream_additional_info": livestream_additional_info,
            "current_time": current_time,
        },
    )


def single_livestream(request, pk):
    livestream = get_object_or_404(Livestream, pk=pk)
    current_time = datetime.now(pytz.utc)

    time_in_relation_to_sunrise = get_sunrise_time_relationship(livestream)

    return render(
        request,
        "alwayssunriseapp/single_livestream.html",
        {
            "livestream": livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
        },
    )
