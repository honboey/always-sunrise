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
    try:
        latitude = geocode_result[0]["geometry"]["location"]["lat"]
        longitude = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        print("There's an error in getting the lat and long")
        return None
    return (latitude, longitude)
