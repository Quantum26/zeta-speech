import requests
import json
import sys
import os
sys.path.insert(1, '../../')

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')


url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q":"Las Vegas","days":"3"}
with open(os.path.join(path_to_secrets, 'secrets.json'), 'r') as f:
	key = json.load(f)["weather_api_key"]
headers = {
	"X-RapidAPI-Key": key,
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

with open(os.path.join(os.path.dirname(__file__), "weather.json"), 'w') as f:
    f.write(json.dumps(response.json()))
print(response.json()['current'])