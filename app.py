import numpy as np
import os
import datetime as dt
from dateutil.relativedelta import relativedelta


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
@app.route("/")
def home():
    print("This will return the Home page")
    return(
        f"Welcome to the SQLAlchemy-challenge API!<br/><br/>" 
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results= session.query(measurement.date,measurement.prcp).\
        order_by(measurement.date).all()

    session.close()

    date_prcp = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        date_prcp.append(new_dict)

    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - relativedelta(months = 12)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= query_date)\
    .filter(measurement.station == 'USC00519281').all()
    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

   
    return jsonify(tobs_list)
 
@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    """min_temp, avg_temp, and max_temp per date starting from a starting date.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        
    """

    session = Session(engine)
    return_list = []
    results = session.query(measurement.date, func.min(measurement.tobs), \
                            func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start).\
                        group_by(measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["min_temp"] = min
        new_dict["avg_temp"] = avg
        new_dict["max_temp"] = max
        return_list.append(new_dict)

    session.close()    

    return jsonify(return_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    """min_temp, avg_temp, and max_temp per date starting from a starting date.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        
    """
    session = Session(engine)
    return_list = []

    results = session.query(measurement.date, func.min(measurement.tobs), \
                            func.avg(measurement.tobs), func.max(measurement.tobs)).\
                        filter(measurement.date >= start, measurement.date <= end).\
                        group_by(measurement.date).all()

    for date, min, avg, max in results:
        new_dict = {}
        new_dict["Date"] = date
        new_dict["min_temp"] = min
        new_dict["avg_temp"] = avg
        new_dict["max_temp"] = max
        return_list.append(new_dict)

    session.close()
    return jsonify(return_list)

if __name__ == "__main__":
    app.run(debug=True)


