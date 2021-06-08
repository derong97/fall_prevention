import requests

baseURL = "http://localhost:3000/current_patient_details/1"
x = requests.get(baseURL)

print(x.text)

y = requests.patch(baseURL, data = {"fallRiskStatus" : "mod"})

print(y.text)
