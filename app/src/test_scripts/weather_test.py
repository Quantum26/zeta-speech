import requests
import json
import sys
sys.path.insert(1, '../')

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q":"Las Vegas","days":"3"}

headers = {
	"X-RapidAPI-Key": "081475fe84mshc57f65e5920ea51p184774jsn89e436c1bc72",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

with open("weather.json", 'w') as f:
    f.write(json.dumps(response.json()))
print(response.json())