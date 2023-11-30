# __sqlalchemy-challenge__

## __SQLAlchemy Climate Analysis and Flask API__

__Overview__

This project, aims to provide a climate analysis and a Flask API for retrieving weather data from a SQLite database containing climate data from Honolulu, Hawaii. The analysis includes querying the database using SQLAlchemy to perform various analyses and creating a Flask API to access this data.

## __Files Included__

[climate_starter.ipynb](https://github.com/kaijaygregory/sqlalchemy-challenge/blob/main/climate_starter.ipynb): This Jupyter notebook contains the initial analysis using Python, SQLAlchemy, Pandas, and Matplotlib to explore and analyze climate data.

[app.py](https://github.com/kaijaygregory/sqlalchemy-challenge/blob/main/app.py): This file serves as the main script to create a Flask API, defining routes to access different data points.

__Resources:__ This directory contains the data files used for the analysis, including the SQLite database file (hawaii.sqlite).

## __Part 1: Analyze and Explore the Climate Data__

The climate_starter.ipynb notebook uses SQLAlchemy to connect to the SQLite database and conducts an in-depth analysis. It performs precipitation and station analyses, calculating various statistics and creating visualizations using Matplotlib.
![Precipitation Analysis](https://github.com/kaijaygregory/sqlalchemy-challenge/blob/main/Images/Precipitation%20Analysis.png)
![Station Analysis](https://github.com/kaijaygregory/sqlalchemy-challenge/blob/main/Images/Station%20Analysis.png)

## __Part 2: Design Your Climate App__

The app.py file creates various routes to access the climate data stored in the SQLite database.
The following routes have been implemented:
* /: Homepage displaying available routes.
* /api/v1.0/precipitation: Returns JSON representation of precipitation data for the last 12 months.
* /api/v1.0/stations: Returns a JSON list of weather stations in the dataset.
* /api/v1.0/tobs: Provides JSON list of temperature observations for the most active station for the previous year.
* /api/v1.0/<start> and /api/v1.0/<start>/<end>: Returns JSON list of temperature statistics for a specified start date or date range.







