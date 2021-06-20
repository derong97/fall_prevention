import flask
import sys
from algorithm import startAlgo, stopAlgo
import data
from flask import request, render_template, jsonify 
from flask_cors import CORS
import threading
from sqlalchemy import create_engine

app = flask.Flask("__main__")
CORS(app)

sql_engine = create_engine("mysql+pymysql://raspberry:password@10.21.147.2/post_monitoring_db")
sql_conn = sql_engine.connect()

@app.route("/")
def frontend():
    return flask.render_template("index.html")

@app.route("/patient-information", methods=["POST", "GET", "PATCH", "DELETE"])
def json():
    
    if request.method == "GET":
        print("get called", data.FALL_RISK_STATUS)
        
        return jsonify({"fall_risk_status": data.FALL_RISK_STATUS}), 200
      
    elif request.method == "POST": 
        content = request.json
#         data.TIME_STARTED = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        startAlgo(content["bed_number"], content["patient_accompanied"])
        return "", 200

    elif request.method == "PATCH": 
        print("patch api called")
        #to update fall risk status 
        content = request.json
        print(content)
        data.FALL_RISK_STATUS = content["fall_risk_status"]
        return "", 200

    elif request.method == "DELETE":
        args = request.args
        isAbort = args['key1']
        stopAlgo(isAbort)
        return "", 200

# Enable page refresh
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
