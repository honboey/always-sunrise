import math
import pytz

from django.shortcuts import render, get_object_or_404

from alwayssunriseapp.utils.api_retrievals import get_weather
from .models import Livestream
from datetime import datetime, timedelta

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


def get_next_sunrise_livestream(livestream_queryset):
    """
    Queryset -> Livestream
    Given a queryset of livestreams, choose the livestream which is closest to its upcoming sunrise
    """
    # Get the current time in UTC
    current_time = datetime.now(pytz.timezone("UTC"))
    future_sunrise_livestreams = livestream_queryset.filter(
        sunrise_time_tomorrow__gt=datetime.now(pytz.timezone("UTC"))
    )
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
    for livestream in future_sunrise_livestreams:
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


def center_current_livestream_in_list(livestreams, current_livestream):
    """ "
    Given a queryset of livestreams, sort them in a way where the current livestream is in the middle of the list
    """
    livestream_list = list(livestreams.order_by("sunrise_time_today"))
    number_of_livestreams = len(livestream_list)
    index_of_current_livestream = livestream_list.index(current_livestream)
    if index_of_current_livestream + 1 == math.ceil(number_of_livestreams / 2):
        sorted_livestreams = livestream_list
        return sorted_livestreams
    elif index_of_current_livestream + 1 < math.ceil(number_of_livestreams / 2):
        list_tail = livestream_list[
            -(
                math.ceil(number_of_livestreams / 2) - (index_of_current_livestream + 1)
            ) :
        ]
        list_head = livestream_list[: len(livestream_list) - len(list_tail)]
        sorted_livestreams = list_tail + list_head
        return sorted_livestreams
    else:
        list_tail = livestream_list[
            : (index_of_current_livestream + 1) - math.ceil(number_of_livestreams / 2)
        ]
        list_head = livestream_list[-(len(livestream_list) - len(list_tail)) :]
        sorted_livestreams = list_head + list_tail
        return sorted_livestreams


# Create your views here.


def index(request):
    livestreams = Livestream.objects.all()
    current_time = datetime.now(pytz.utc)

    # Get correct livestream
    upcoming_livestream = get_next_sunrise_livestream(livestreams)

    # Create string of time difference
    time_in_relation_to_sunrise = get_sunrise_time_relationship(upcoming_livestream)

    # Get weather
    weather = get_weather(upcoming_livestream)

    return render(
        request,
        "alwayssunriseapp/index.html",
        {
            "livestream": upcoming_livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
            "weather": weather
        },
    )

    # Get current weather for livestream
    # weather = get_weather(upcoming_livestream)

def livestream_list(request):
    livestreams = Livestream.objects.all()
    current_livestream = get_next_sunrise_livestream(livestreams)
    sorted_livestreams = center_current_livestream_in_list(
        livestreams, current_livestream
    )

    current_time = datetime.now(pytz.utc)
    livestream_additional_info = []

    for livestream in sorted_livestreams:
        if livestream == current_livestream:
            livestream_additional_info.append(
                {
                    "livestream": livestream,
                    "time_in_relation_to_sunrise": get_sunrise_time_relationship(
                        livestream
                    ),
                    "weather": get_weather(livestream),
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
                    "weather": get_weather(livestream),
                }
            )

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

    weather = get_weather(livestream)

    return render(
        request,
        "alwayssunriseapp/single_livestream.html",
        {
            "livestream": livestream,
            "current_time": current_time,
            "time_in_relation_to_sunrise": time_in_relation_to_sunrise,
            "weather": weather,
        },
    )
