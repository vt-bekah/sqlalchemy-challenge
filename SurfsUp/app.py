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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Date range available is from 2010-01-01 to 2017-08-23<br/>"
        f"Enter start date of format '/api/v1.0/YYYY-MM-DD':<br/> /api/v1.0/<start><br/>"
        f"Enter start date / end date using this format '/api/v1.0/YYYY-MM-DD/YYYY-MM-DD':<br/> /api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query only the last 12 months of precipitation data and store it
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    precip_12mo = session.query(measurement.date, measurement.prcp).\
                    filter(measurement.date>=year_ago).\
                    filter(measurement.prcp!="NaN").\
                    order_by(measurement.date).all()
    
    # Close session (rest of manipulation outside DB)
    session.close()

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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query only the last 12 months of dates and temperature observations of the most-active station and store it
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    USC00219281_temp_12mo = session.query(measurement.date, measurement.tobs).\
                                filter(measurement.date>=year_ago).\
                                filter(measurement.station=='USC00519281').\
                                filter(measurement.tobs!="NaN").\
                                order_by(measurement.date).all()
    
    # Close session (rest of manipulation outside DB)
    session.close()

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
        startdate = dt.datetime.strptime(start, '%Y-%m-%d')
        # Check startdate is within possible date range
        if startdate >= data_begin and startdate <= data_end:
        
            # Create our session (link) from Python to the DB
            session = Session(engine)
            # Query the temperatures from the start date calculating min, max, average
            stats = session.query(func.min(measurement.tobs), 
                                func.max(measurement.tobs), 
                                func.avg(measurement.tobs)).\
                                    filter(measurement.date>=start).all()           
            # Close session (rest of manipulation outside DB)
            session.close()
            
            # Convert list of tuples into a regular list
            stat_list = [item for t in stats for item in t]

            # Return a JSON min, max, avg list of stations from the dataset.
            return jsonify(stat_list)
        
        return jsonify({"error": f"Given start date, {start}, is outside available data, {data_begin.date()} to {data_end.date()}."}), 404
    except (ValueError):
        return jsonify({"error": f"Given start date, {start}, is not the correct format 'YYYY-MM-DD'"}), 404
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_stats(start,end):
    try:
        # If date is the wrong format, handle exception and indicate as such
        startdate = dt.datetime.strptime(start, '%Y-%m-%d')
        enddate = dt.datetime.strptime(end, '%Y-%m-%d')
        # Check startdate is within possible date range
        if startdate <= enddate:
            if startdate >= data_begin and startdate <= data_end and enddate >= data_begin and enddate <= data_end:
            
                # Create our session (link) from Python to the DB
                session = Session(engine)
                # Query the temperatures from the start date calculating min, max, average
                stats = session.query(func.min(measurement.tobs), 
                                    func.max(measurement.tobs), 
                                    func.avg(measurement.tobs)).\
                                        filter(measurement.date>=start).\
                                        filter(measurement.date<=end).all()           
                # Close session (rest of manipulation outside DB)
                session.close()
                
                # Convert list of tuples into a regular list
                stat_list = [item for t in stats for item in t]

                # Return a JSON min, max, avg list of stations from the dataset.
                return jsonify(stat_list)
            
            return jsonify({"error": f"Given dates, {start} or {end}, is outside available data, {data_begin.date()} to {data_end.date()}."}), 404
        else:
            return jsonify({"error": f"Given start date, {start}, is after the end date, {end}."}), 404
    except (ValueError):
        return jsonify({"error": f"Given date(s), {start} and/or {end}, is not the correct format 'YYYY-MM-DD'"}), 404
    

if __name__ == "__main__":
    app.run(debug=True)
