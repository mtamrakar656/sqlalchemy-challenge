import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
Stations = Base.classes.station

##################################################
# Flask Setup
##################################################
app = Flask(__name__)

##################################################
# Flask Routes
##################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]</br>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session(link) from Python to the DB
    session = Session(engine)

    """Return a list of last 12 months of Precipitation data"""
    # Query Precipitation for last 12 months
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation_data
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session(link) from Python to the DB
    session = Session(engine)

    """Return a list of last 12 months of Precipitation data"""
    # Query all Stations
    station_query = session.query(Stations.station, Stations.name).all()
        

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation_data
    stations_data = []
    for station, name in station_query:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_data.append(stations_dict)

    return jsonify(stations_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session(link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temperature observations of the most active station station
    for the last year of data"""
    
    # Query the most recent data in the dataset
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    # Query date 12 months prior
    last_year_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') \
        - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query date and temperature values
    temperature_query = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= last_year_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation_data
    temperature_data = []
    for date, tobs in temperature_query:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temperature"] = tobs
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)



if __name__ == '__main__':
    app.run(debug=True)