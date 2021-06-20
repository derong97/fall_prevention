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

@app.route("/")
def frontend():
    return flask.render_template("index.html")

@app.route("/patient-information", methods=["POST", "GET", "PATCH", "DELETE"])
def json():
    
    if request.method == "GET":
        print("get called", data.FALL_RISK_STATUS)
        
        return jsonify({"fall_risk_status": data.FALL_RISK_STATUS}), 200
      
    elif request.method == "POST":
        print("post called")
        content = request.json
        print("bed number: ", content["bed_number"])
        print("patient accompanied: ", content["patient_accompanied"])
        print("toileting session is starting...") 
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
#         args = request.args
#         print(args.items())
        content = request.json
        print(content)
        isAbort = content["is_abort"]
        isAccompanied = content["is_accompanied"]
        stopAlgo(isAbort, isAccompanied)
        return "", 200

# Enable page refresh
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
