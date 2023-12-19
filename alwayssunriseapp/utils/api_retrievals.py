import googlemaps
import os
import requests
import pytz
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

gmaps = googlemaps.Client(key=google_maps_api_key)


def get_lat_and_long(location_string):
    """
    Given a location string, call the Geocode API and retrieve its lat and long.
    """
    geocode_result = gmaps.geocode(location_string)
    try:
        latitude = geocode_result[0]["geometry"]["location"]["lat"]
        longitude = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        print("There's an error in getting the lat and long")
        return None
    return (latitude, longitude)


def get_timezone(latlongtuple):
    """
    Given the lat and long, retrieve the timezone.
    """
    try:
        timezone_result = gmaps.timezone(latlongtuple)
    except:
        print("There's an error")
    return timezone_result["timeZoneId"]


def get_sunrise_times(day, latlongtuple):
    """
    Given the lat and long, retrieve sunrise times for the specified day.
    """
    response = requests.get(
        f"https://api.sunrisesunset.io/json?lat={latlongtuple[0]}&lng={latlongtuple[1]}&date={day}"
    )

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
    return local_timezone.localize(naive_sunrise_datetime)


def get_weather(livestream):
    """
    Given the lat and long, retrieve the current weather, the ...
    """
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={livestream.latitude},{livestream.longitude}"
    )
    weather_json = response.json()
    print(json.dumps(weather_json, indent=2))
    return weather_json
