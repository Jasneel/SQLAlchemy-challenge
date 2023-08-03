import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

################################################
# Database Setup
#################################################
engine = create_engine("sqlite://///Users/jasneel/Desktop/UofT Data Analytics Bootcamp/Homework Assignments/Module 10 SQLAlchemy/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    """List all available API Routes"""
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year_date).all()

    precipitation_list = []

    for row in results:
        date_dict = {}
        date_dict[row.date] = row.prcp
        precipitation_list.append(date_dict)

    return jsonify(precipitation_list)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station).all()
    station_list = list(np.ravel(results))
    
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= last_year_date).all()
    most_active_data = list(np.ravel(results))
    
    return jsonify(most_active_data)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    temp_list = []
    for date, min_temp, avg_temp, max_temp in results:
        temp_dict = {
            'Date': date,
            'TMIN': min_temp,
            'TAVG': avg_temp,
            'TMAX': max_temp
        }
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start, end):
    results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).group_by(measurement.date).all()

    temp_list = []
    for date, min_temp, avg_temp, max_temp in results:
        temp_dict = {
            'Date': date,
            'TMIN': min_temp,
            'TAVG': avg_temp,
            'TMAX': max_temp
        }
        temp_list.append(temp_dict)

    return jsonify(temp_list)

# Call Flask to run
if __name__ == '__main__':
    app.run(debug=True)
