from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os

#SQLAlchemy
#Set Base
Base = automap_base()

#Set connection
file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
file_path = os.path.join(file_dir, 'Resources', 'hawaii.sqlite')
db_path = f"sqlite:///{file_path}"
print(db_path)
engine = create_engine(db_path)
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

#Reflect tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask
# Set up app
app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return (
        f"Weather information<br/><br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation : gives precipitation information<br/>"
        f"/api/v1.0/stations : lists available stations<br/>"
        f"/api/v1.0/tobs : lists temperature observations<br/>"
        f"/api/v1.0/&lt;start&gt; and /api/v1.0/&lt;start&gt;/&lt;end&gt; : temperature information between dates<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Get data
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Define empty dictionary
    result_dict = {}

    # Convert data to dictionary
    for row in results:
        result_dict[row[0]] = row[1]

    return(jsonify(result_dict))

@app.route("/api/v1.0/stations")
def stations():
    # Get data
    session = Session(engine)
    results = (session
            .query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)
            .all()
    )
    session.close()

    # Define list
    results_list = []
    for result in results:
        res_dict = {}
        res_dict['id'] = result[0]
        res_dict['station'] = result[1]
        res_dict['name'] = result[2]
        res_dict['latitude'] = result[3]
        res_dict['longitude'] = result[4]
        res_dict['elevation'] = result[5]
        results_list.append(res_dict)

    # Return JSON
    return(jsonify(results_list))

@app.route("/api/v1.0/tobs")
def tobs():
    return("Temperature")

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp(start, end):
    return("Start/end")

if __name__ == '__main__':
    app.run(debug=True)