from django.shortcuts import render
from django.utils import timezone
from .models import Livestream

# Create your views here.


def index(request):
    livestream = Livestream.objects.get(location__contains="Tokyo")
    return render(request, "alwayssunriseapp/index.html", {"livestream": livestream})


def livestream_list(request):
    livestreams = Livestream.objects.filter(
        local_sunrise_time__lte=timezone.now()
    ).order_by("local_sunrise_time")
    return render(
        request, "alwayssunriseapp/livestream_list.html", {"livestreams": livestreams}
    )
