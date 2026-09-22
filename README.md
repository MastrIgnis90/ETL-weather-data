**Currently in the middle of a rewrite to leverage Pyspark. May not work as expected until this rewrite is finished**
Currently only works with open-meteo API.

# Setup
In the config folder you will find 2 files. database.ini and apiRequest.ini. Both files need all of their fields filled out. 
Database.ini requires the name of the postgresql database you want to connect to, along with the username, password, and the location of the database.
apiRequest.ini requires parameters from open-meteo to properly make the API request. This includes latitude, longitude, the start date (in format `YYYY-MM-DD`) and end date (same format)

After filling out the config files the python scripts should work when you run them through CLI. The order to run the scripts is Extract.py -> transform.py -> load.py

