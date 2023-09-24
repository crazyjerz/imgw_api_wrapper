## IMGW API Wrapper for Python
An extremely simple module allowing you to look up current weather forecasts on the territory of Poland using governmental data (https://meteo.imgw.pl/) Currently, the main and only feature is weather data lookup based on coordinates.

### Before using: 
Check if you are allowed to use the API - using it is banned for purposes of economic activity (anything for-profit). 

The author of this package does not endorse and is not responsible for any illegal applications of it.

### How to use:
Install the package using ``pip``:
```
pip install imgw_api_wrapper
```
Data lookup is done by creating an ``IMGW`` object and calling the ``get_data`` method on it with latitude, longitude and model as arguments. For more details about models, visit the official IMGW site.