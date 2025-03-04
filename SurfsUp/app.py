# Import the dependencies.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import os

db_path = os.path.join(os.path.dirname(__file__), "Resources", "hawaii.sqlite")

if not os.path.exists(db_path):
    print("Error: Database file not found!")
else:
    print("Database file found, proceeding...")

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{db_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
# Create an app, being sure to pass __name__
app = Flask(__name__)  

#################################################
# Flask Routes
#################################################

@app.route("/")  
def home():  
    print("Server received request for 'Home' page...") 
    return (
        f"Welcome to my 'Home' page!<br/>" 
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"<br/>"
        f"Note: Use dates in YYYY-MM-DD format for start date and end date parameters."
    ) 

@app.route("/api/v1.0/precipitation") 
def precipitation():
    print("Server received request for 'Precipitation' page...")
    session=Session(engine)

    # Find the most recent date in the data set.
    recent_date = session.query(func.max(Measurement.date)).scalar()

    # Starting from the most recent data point in the database. 
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    one_year_ago = recent_date - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    past_twelve_months = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_year_ago)
        .order_by(Measurement.date)
        .all()
    )

    session.close()

    #Create a dictionary from the past_twelve_months data and append to a list of precipitation
    precipitation = []
    for date, prcp in past_twelve_months:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations") 
def stations():
    print("Server received request for 'Stations' page...")
    session = Session(engine)

    #Query all stations
    stations = session.query(Station.station).all()

    session.close()

    #Convert to list of tuples into normal list
    all_stations = list(np.ravel(stations))

    #Return the list of stations as a JSON response
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs") 
def tobs():
    print("Server received request for 'TOBS' page...")
    session = Session(engine)

    # Find the most recent date in the data set.
    recent_date = session.query(func.max(Measurement.date)).scalar()

    # Starting from the most recent data point in the database. 
    recent_date = dt.datetime.strptime(recent_date, "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    one_year_ago = recent_date - dt.timedelta(days=365)

    # List the stations and their counts in descending order.
    active_station = (
        session.query(Measurement.station, func.count(Measurement.station))
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .all()
    )

    # Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
    most_active_station = active_station[0][0]

    temp_stats = (
    session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    )
    .filter(Measurement.station==most_active_station)
    .all()
    )

    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    past_twelve_months_temp = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date >= one_year_ago)
        .filter(Measurement.station == most_active_station)
        .order_by(Measurement.date)
        .all()
    )

    session.close()

    # Create a list
    tobs_list = [temp[1] for temp in past_twelve_months_temp]

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_start(start, end=None):

    session = Session(engine)

    # Define query
    temp_query = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start)

    # If an end date is provided, add it to the filter
    if end:
        temp_query = temp_query.filter(Measurement.date <= end)

    results = temp_query.all()
    session.close()

    # Unpack results
    tmin, tavg, tmax = results[0]

    # Return the data as JSON
    return jsonify({
        "start_date": start,
        "end_date": end if end else "Latest Available",
        "TMIN": tmin,
        "TAVG": tavg,
        "TMAX": tmax
    })

if __name__ == "__main__":  # Check if the script is being run directly
    app.run(debug=True)  # Run the Flask development server with debug mode enabled