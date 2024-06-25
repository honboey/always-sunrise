# Always Sunrise

Always Sunrise is a Django web app that determines where a sunrise is occuring and plays the closest livestream to that location. It can be found at [always-sunrise.com](http://www.always-sunrise.com/).

## Running the project

1. Clone this project
2. Setup your virtual environment
3. Install the requirements with `pip install -r requirements.txt`
4. Get a Google Geocode API key. [Instructions here](https://developers.google.com/maps/documentation/geocoding/get-api-key).
5. Create a `.env` file and add this API key as follows (no `""` surround your key):
```
GOOGLE_MAPS_API_KEY=<your_key>
```

### How it works

Admins input a list of livestream links from around the world. When a livestream object is created, two API calls are made:
1. The first is to the Google Geocode API which uses its location to return the livestream's exact latitude and longitude.
2. The second is to the SunriseSunset API which sends the aforementioned lat and long and requests the times of the most recent and upcoming sunrise times.

These are then saved to the database.

When a user visits the site, the server decides which livestream to show. This is determined by two factors:
1. Only show a livestream where the sunrise is in the future
2. Only show a livestream where the time to sunrise is the shortest

Because sunrise times change everyday, a daily call is made to the SunriseSunset API to update all livestreams' sunrise times. This occurs at 1:19am (UTC).

## Servers

Always Sunrise is hosted by PythonAnywhere. To run commands on the PythonAnywhere server you will need to open a Bash console in the virtual environment. To do so, in the PythonAnywhere dashboard, go to "Web apps" and click on "Start a console in this virtualenv".

### Useful Commands
• Retrieve sunrise times and add them to your objects:
```
python manage.py sync_livestreams
```
• Run Black (python formatter): 
```
black alwayssunriseapp ./*.py --exclude migrations
```



