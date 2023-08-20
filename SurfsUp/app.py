# Web API module
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
# Data manipulation dependendencies
import datetime as dt

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

##############################################################
# Functions & related variables for common calls into Database
##############################################################

# Set default date filters to include all dates (available dates from 2010-01-01 to 2017-08-03)
default_start=measurement.date>="2010-01-01"
default_end=measurement.date<="2017-08-23"
# Create variable for common year ago timeframe
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Create a function for open, extract, close a session to the DB for 
# 2 columns of data, up to 3 filters, and order by
def two_col_db_pull(col1, col2, order_col, filter1=default_start, filter2=default_start, filter3=default_start): 
    # Create session (link) from Python to the DB
    session = Session(engine)

    data_pull = session.query(col1, col2).\
                                filter(filter1).\
                                filter(filter2).\
                                filter(filter3).\
                                order_by(order_col).all()

    # Close session (rest of manipulation outside DB)
    session.close()

    return(data_pull)

# Create a function for open, extract, close a session to the DB to gather 
# minimum, maximum, and average of a singgle column of data that can be 
# filtered by start and end dates (available dates from 2010-01-01 to 2017-08-03)
def min_max_avg_dates(column, start_date="2010-01-01", end_date="2017-08-03"):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the temperatures from the start date calculating min, max, average
    stats = session.query(func.min(column), 
                        func.avg(column), 
                        func.max(column)).\
                            filter(measurement.date>=start_date).\
                            filter(measurement.date<=end_date).all()           
    # Close session (rest of manipulation outside DB)
    session.close()

    # Convert list of tuples into a regular list
    stat_list = [item for t in stats for item in t]

    return (stat_list)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate App<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Convert the query results from your 12mo precipitation analysis:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Return a JSON list of stations from the dataset.<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Query the dates and temperature observations of the most-active station for the previous year of data.<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Return minimum temperature, average temperature, maximum temperature for a specified start or start-end range.<br/>"
        f"Date range available is from 2010-01-01 to 2017-08-23<br/>"
        f"Enter start date of format '/api/v1.0/YYYY-MM-DD':<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Enter start date / end date using this format '/api/v1.0/YYYY-MM-DD/YYYY-MM-DD':<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Pull data using function
    precip_12mo = two_col_db_pull(measurement.date, 
                                  measurement.prcp, 
                                  measurement.date, 
                                  measurement.date>=year_ago, 
                                  measurement.prcp!="NaN")

    # Convert list of tuples into a dictionary
    precip_dict = dict()
    for date, prcp in precip_12mo:
        precip_dict.setdefault(date, []).append(prcp)

    # Return a JSON list of stations from the dataset.
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the list of stations
    station_list = session.query(measurement.station).distinct().all()

    # Close session (rest of manipulation outside DB)
    session.close()

    # Convert list of tuples into a regular list
    stations = [item for t in station_list for item in t]

    # Return a JSON list of stations from the dataset.
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():    
    # Pull data using function
    USC00219281_temp_12mo = two_col_db_pull(measurement.date, 
                                            measurement.tobs, 
                                            measurement.date, 
                                            measurement.date>=year_ago, 
                                            measurement.station=='USC00519281', 
                                            measurement.tobs!="NaN")

    # Convert list of tuples into a regular list
    USC00519281_temps = [item for t in USC00219281_temp_12mo for item in t]

    # Return a JSON list of stations from the dataset.
    return jsonify(USC00519281_temps)

# Date range available is from 2010-01-01 to 2017-08-03
data_begin = dt.datetime.strptime("2010-01-01", '%Y-%m-%d')
data_end = dt.datetime.strptime("2017-08-23", '%Y-%m-%d')

@app.route("/api/v1.0/<start>")
def start_stats(start):
    try:
        # If date is the wrong format, handle exception and indicate as such
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        # Check startdate is within possible date range
        if start_date >= data_begin and start_date <= data_end:
        
            # Pull data using function
            stats = min_max_avg_dates(measurement.tobs, start)

            # Return a JSON min, max, avg list of stations from the dataset.
            return jsonify(stats)
        
        return jsonify({"error": f"Given start date, {start}, is outside available data, {data_begin.date()} to {data_end.date()}."}), 404
    except (ValueError):
        return jsonify({"error": f"Given start date, {start}, is not the correct format 'YYYY-MM-DD'"}), 404
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_stats(start,end):
    try:
        # If date is the wrong format, handle exception and indicate as such
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
        # Check startdate is within possible date range
        if start_date <= end_date:
            if start_date >= data_begin and start_date <= data_end and end_date >= data_begin and end_date <= data_end:
            
                # Pull data using function
                stats = min_max_avg_dates(measurement.tobs, start, end)
                
                # Return a JSON min, max, avg list of stations from the dataset.
                return jsonify(stats)
            
            return jsonify({"error": f"Given dates, {start} or {end}, is outside available data, {data_begin.date()} to {data_end.date()}."}), 404
        else:
            return jsonify({"error": f"Given start date, {start}, is after the end date, {end}."}), 404
    except (ValueError):
        return jsonify({"error": f"Given date(s), {start} and/or {end}, is not the correct format 'YYYY-MM-DD'"}), 404
    

if __name__ == "__main__":
    app.run(debug=True)
