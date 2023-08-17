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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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

# @app.route("/api/v1.0/justice-league/<real_name>")
# def justice_league_character(real_name):
#     canonicalized = real_name.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()
#         if search_term == canonicalized:
#             return jsonify(character)
#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
