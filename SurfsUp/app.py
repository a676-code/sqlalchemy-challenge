# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def index():
    return """
<strong>Available routes:</strong></br>
<a href=http://127.0.0.1:5000/api/v1.0/precipitation>
    /api/v1.0/precipitation
</a><br>
<a href="http://127.0.0.1:5000/api/v1.0/stations">
    /api/v1.0/stations
</a><br>
<a href="http://127.0.0.1:5000/api/v1.0/tobs">
    /api/v1.0/tobs
</a><br>
<a href="http://127.0.0.1:5000/api/v1.0/&lt;start&gt;">
    /api/v1.0/&lt;start&gt;
</a><br>
<a href="http://127.0.0.1:5000/api/v1.0/&lt;start&gt;/&lt;end&gt;">
    /api/v1.0/&lt;start&gt;/&lt;end&gt;
</a>
"""

@app.route('/api/v1.0/precipitation')
def precipitation():    
    last_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()
    return jsonify(dict(last_year))
    
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)
    
@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.date).all()
    return jsonify(results)
    
@app.route('/api/v1.0/<start>')
def start_(start):
    
    start = dt.strptime(start, "%Y-%m-%d")
    
    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    temps = []
    new_dict = {}
    for Min, Avg, Max in temperatures:
        new_dict['Min'] = Min
        new_dict['Avg'] = Avg
        new_dict['Max'] = Max
    temps.append(new_dict)

    return jsonify(temps)
    
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    
    start = dt.strptime(start, "%Y-%m-%d")
    end = dt.strptime(end, "%Y-%m-%d")
    
    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
        
    temps = []
    new_dict = {}
    for Min, Avg, Max in temperatures:
        new_dict['Min'] = Min
        new_dict['Avg'] = Avg
        new_dict['Max'] = Max
    temps.append(new_dict)
    
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)