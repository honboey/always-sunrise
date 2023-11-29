from django.shortcuts import render
from django.utils import timezone
from .models import Livestream
from datetime import datetime, timedelta

import pytz

# Create your views here.


def index(request):
    livestream = Livestream.objects.get(location__contains="Tokyo")
    current_time = datetime.now(pytz.timezone(livestream.timezone))
    time_difference = current_time - livestream.sunrise_time_today

    # Create string of time difference
    def format_time_after_sunrise(timedelta_object):
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

    time_in_relation_to_sunrise = format_time_after_sunrise(time_difference)

    print(time_in_relation_to_sunrise)

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
        local_sunrise_time__lte=timezone.now()
    ).order_by("local_sunrise_time")
    return render(
        request, "alwayssunriseapp/livestream_list.html", {"livestreams": livestreams}
    )
