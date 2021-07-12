import numpy as np

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
station = Base.classes.station

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
    # Query all Precipitation
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date>= "2016-08-23").all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation_data
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

if __name__ == '__main__':
    app.run(debug=True)