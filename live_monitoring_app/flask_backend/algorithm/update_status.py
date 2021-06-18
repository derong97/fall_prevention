from flask import jsonify
import requests
import time

baseURL = "http://127.0.0.1:5000"
endpoint = "/patient-information"
apiURL = baseURL + endpoint

print(apiURL)

x = requests.get(apiURL)

print(x.text)

fallUpdate = {'fall_risk_status': 'fall'}
lowRiskUpdate = {'fall_risk_status': 'low'}
modRiskUpdate = {'fall_risk_status': 'mod'}
highRiskUpdate = {'fall_risk_status': 'high'}
tamUpdate = {'fall_risk_status': 'tam'}

while True:
    y = requests.patch(apiURL, json = modRiskUpdate)
    print(y.text)
    time.sleep(6)
    y = requests.patch(apiURL, json = highRiskUpdate)
    print(y.text)
    time.sleep(6)
    y = requests.patch(apiURL, json = fallUpdate)
    print(y.text)
    time.sleep(6)