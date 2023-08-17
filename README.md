# sqlalchemy-challenge
This repository contains challenge files for UT DAV Bootcamp Module 10 Advanced SQL

# File Notes
* SurfsUp folder contains the solution and resource files for the Module 10 challenge
  * climate.ipynb contains the solution to Part 1: Analyze and Explore the Climate Data
  * app.py contains the solution to Part2: Design Your Climate App
  * Resources folder contains the SQL Lite database and related tables provided with the starter code
* Starter_Code folder contains the files provided in BCS/Canvas for completing the challenge.
   

# References
The following references were used in creating the solution within the SurfsUp folder:
 * https://stackoverflow.com/questions/17578115/pass-percentiles-to-pandas-agg-function used as a reference for pulling in quartiles to the aggregate function for dataframe statistics
 


# Challenge Instructions

## Setup
1. Create a new repository for this project called sqlalchemy-challenge. Do not add this assignment to an existing repository.
2. Clone the new repository to your computer.
3. Inside your local Git repository, create a directory for this Challenge. Use a folder name that corresponds to the Challenge, such as SurfsUp.
4. Add your Jupyter notebook and app.py to this folder. They’ll contain the main scripts to run for analysis. Also add the Resources folder, which contains the data files you will be using for this challenge.
5. Push the changes to GitHub or GitLab.

## Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:
1. Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.
2. Use the SQLAlchemy create_engine() function to connect to your SQLite database.
3. Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
4. Link Python to the database by creating a SQLAlchemy session.
**IMPORTANT**: Remember to close your session at the end of your notebook.
5. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
### Precipitation Analysis
1. Find the most recent date in the dataset.
2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Select only the "date" and "prcp" values.
4. Load the query results into a Pandas DataFrame. Explicitly set the column names.
5. Sort the DataFrame values by "date".
6. Plot the results by using the DataFrame plot method
7. Use Pandas to print the summary statistics for the precipitation data.
### Station Analysis
1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
     * List the stations and observation counts in descending order.
     * Answer the following question: which station id has the greatest number of observations?
3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
     * Filter by the station that has the greatest number of observations.
     * Query the previous 12 months of TOBS data for that station.
     * Plot the results as a histogram with bins=12, as the following image shows:
5. Close your session.

## Part 2: Design Your Climate App
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
1. /
     * Start at the homepage.
     * List all the available routes.
2. /api/v1.0/precipitation
     * Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
     * Return the JSON representation of your dictionary.
3. /api/v1.0/stations
     * Return a JSON list of stations from the dataset.
4. /api/v1.0/tobs
     * Query the dates and temperature observations of the most-active station for the previous year of data.
     * Return a JSON list of temperature observations for the previous year.
5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
     * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
     * For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
     * For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

# Getting Started

## Prerequisites
You must have python, jupyter notebok / lab, conda, flask, matplotlib, numpy, pandas, sqlalchemy, datetime 

## Cloning Repo
$ git clone https://github.com/vt-bekah/sqlalchemy-challenge.git

$ cd sqlalchemy-challenge

# Built With
* Python v3.10.11
* jupyter notebook v6.5.2
* jupyterlab v3.6.3
* conda v23.5.0
* Flask v2.2.2
**Python Modules**
* matplotlib v3.7.1
* numpy v1.24.3
* pandas v1.5.3
* sqlalchemy v1.4.39
* datetime (native to Python)
