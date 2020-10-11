import numpy as np
import os

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



if __name__ == "__main__":
    app.run(debug=True)


