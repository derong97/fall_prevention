import flask
import sys
from start_algorithm import algo
from flask import request, render_template, jsonify 
from flask_cors import CORS
from flask_mqtt import Mqtt

# sys.path.insert(1, '../algorithm')
# import start_algorithm


app = flask.Flask("__main__")
CORS(app)

# #setup MQTT 
# app.config['MQTT_BROKER_URL'] = '127.0.0.1'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = 'raspberry'
# app.config['MQTT_PASSWORD'] = 'password'
# app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
# mqtt = Mqtt(app)

data = {
    "bed_number": 0,
    "time_started": 0,
    "time_end": 0,
    "hfr_count": 0,
    "patient_accompanied": 0,
    "fall_risk_status": "tam"
}

@app.route("/")
def frontend():
    return flask.render_template("index.html")

@app.route("/patient-information", methods=["POST", "GET", "PATCH", "DELETE"])
def json():
    global data
    if request.method == "GET":
        return jsonify(data), 200
      
    elif request.method == "POST": 
        content = request.json
        data["bed_number"] = content["bed_number"]
        data["time_started"] = content["time_started"]
        data["patient_accompanied"] = content["patient_accompanied"]
        x = algo()
        return jsonify(data), 200

    elif request.method == "PATCH": 
        print("patch api called")
        #to update fall risk status 
        content = request.json
        print(content)
        data["fall_risk_status"] = content["fall_risk_status"]
        return jsonify(data), 200

    elif request.method == "DELETE": 
        data = {
            "bed_number": 0,
            "time_started": 0,
            "time_end": 0,
            "hfr_count": 0,
            "patient_accompanied": 0,
            "fall_risk_status": "low"
        }
        return "", 200

# #MQTT for starting and stopping the algo 
# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     mqtt.subscribe('home/mytopic')


# Enable page refresh
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

app.run(port=5000, debug=True)


# if __name__ == '__main__':
#     app.run()