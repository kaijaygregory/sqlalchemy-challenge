# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import datetime, timedelta, date

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement 
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/start<br/>"
        f"api/v1.0/start/end"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).\
        order_by(measurement.date).all()
        
    precipitation_dict = dict(precipitation)
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(station.station).all()
    station_list = list(np.ravel(stations_data))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query to find the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the last date in the dataset
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query to retrieve temperature observations for the last 12 months from the most active station
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_ago).\
        filter(measurement.station == most_active_station).\
        order_by(measurement.date).all()
    
    # Convert the query result into a list of dictionaries for each observation
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
        
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):
    try:
        
        # Convert the provided start date into a datetime object
        start_date = datetime.strptime(start, "%Y-%m-%d")
        start_behind = start_date - timedelta(days=1)
        start_date = start_behind.date()

        # Query to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to start_date
        temperature_stats = session.query(measurement.date,
                                func.min(measurement.tobs).label('min_temp'),
                                func.avg(measurement.tobs).label('avg_temp'),
                                func.max(measurement.tobs).label('max_temp')).\
            filter(measurement.date >= start_behind).\
            group_by(measurement.date).all()
            
        # Creating a list to hold temperature data for each date
        result_data = []
        for stat in temperature_stats:
            date_str, tmin, tavg, tmax = stat
            temperature_data = {
                "Date": date_str,
                "Minimum Temperature": tmin,
                "Average Temperature": tavg,
                "Maximum Temperature": tmax
            }
            result_data.append(temperature_data)
        
        return jsonify(result_data) if result_data else jsonify([])
    
    except ValueError:
        return jsonify({"error": "Invalid start date format. Please use 'YYYY-MM-DD' format."}), 400
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    try:
        
        # Convert the provided start and end dates into datetime objects
        start_date = datetime.strptime(start, "%Y-%m-%d")
        start_behind = start_date - timedelta(days=0)
        start_date = start_behind.date()
        end_date = datetime.strptime(end, "%Y-%m-%d")
        
        # Query to calculate TMIN, TAVG, and TMAX for all dates greater than or equal to start_date
        temperature_stats = session.query(measurement.date,
                                func.min(measurement.tobs).label('min_temp'),
                                func.avg(measurement.tobs).label('avg_temp'),
                                func.max(measurement.tobs).label('max_temp')).\
            filter(measurement.date >= start_date).\
            filter(measurement.date <= end_date).\
            group_by(measurement.date).all()
            
        # Creating a list to hold temperature data for each date
        result_data = []
        for stat in temperature_stats:
            date_str, tmin, tavg, tmax = stat
            temperature_data = {
                "Date": date_str,
                "Minimum Temperature": tmin,
                "Average Temperature": tavg,
                "Maximum Temperature": tmax
            }
            result_data.append(temperature_data)
        
        return jsonify(result_data) if result_data else jsonify([])
    
    except ValueError:
        return jsonify({"error": "Invalid start or end date format. Please use 'YYYY-MM-DD' format."}), 400

if __name__ == '__main__':
    app.run(debug=True)