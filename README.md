# Always Sunrise

Always Sunrise is a Django web app that determines where a sunrise is occuring and plays the closest livestream to that location. It can be found at [hon.pythonanywhere.com](http://hon.pythonanywhere.com/).

## Servers

Always Sunrise is hosted by PythonAnywhere. To run commands on the PythonAnywhere server you will need to open a Bash console in the virtual environment. To do so, in the PythonAnywhere dashboard, go to "Web apps" and click on "Start a console in this virtualenv".

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


### Useful Commands
• Retrieve sunrise times and add them to your objects:
```
python manage.py sync_livestreams
```
• Run Black (python formatter): 
```
black alwayssunriseapp ./*.py --exclude migrations
```

The designs:
https://xd.adobe.com/view/541b4400-e7d1-4331-a90a-7c6d0b698075-0148/



