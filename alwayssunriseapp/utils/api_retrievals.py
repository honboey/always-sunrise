import googlemaps
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")


def get_lat_and_long(location_string):
    """
    Given a location string, call the Geocode API and retrieve its lat and long.
    """
    gmaps = googlemaps.Client(key=google_maps_api_key)

    geocode_result = gmaps.geocode(location_string)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitute = geocode_result[0]["geometry"]["location"]["lng"]
    print(latitude, longitute)
