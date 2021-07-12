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
def home():
    """List all available api routes."""
    return (
        f"Available Routes for Climate App:<br/>"
        f"------------------------------------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br/>"
        f"Please replace 'start_date' and 'end_date' with your dates (Format: 'YYYY-MM-DD')"
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

@app.route("/api/v1.0/<start>")
def start_temp_range(start):
    # Create our session(link) from Python to the DB
    session = Session(engine)

    """Return TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    
    # Query the min, avg, max of the temperatures for the given start date
    start_temp_range_query = session.query(measurement.date, \
        func.min(measurement.tobs), \
        func.avg(measurement.tobs), \
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        group_by(measurement.date).all()
        
    # Create a dictionary from the row data and append to a list of precipitation_data
    start_temp_data = []
    for date, min, avg, max in start_temp_range_query:
        start_temp_dict = {}
        start_temp_dict["Date"] = date
        start_temp_dict["TMIN"] = min
        start_temp_dict["TAVG"] = avg
        start_temp_dict["TMAX"] = max
        start_temp_data.append(start_temp_dict)

    return jsonify(start_temp_data)

    session.close()

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp_range(start,end):
    # Create our session(link) from Python to the DB
    session = Session(engine)

    """Return TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    
    # Query the min, avg, max for dates between the start and end date inclusive
    start_end_temp_range_query = session.query(measurement.date, \
        func.min(measurement.tobs), \
        func.avg(measurement.tobs), \
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        group_by(measurement.date).all()
        
    # Create a dictionary from the row data and append to a list of precipitation_data
    start_end_temp_data = []
    for date, min, avg, max in start_end_temp_range_query:
        start_end_temp_dict = {}
        start_end_temp_dict["Date"] = date
        start_end_temp_dict["TMIN"] = min
        start_end_temp_dict["TAVG"] = avg
        start_end_temp_dict["TMAX"] = max
        start_end_temp_data.append(start_end_temp_dict)

    return jsonify(start_end_temp_data)

    session.close()

if __name__ == '__main__':
    app.run(debug=True)