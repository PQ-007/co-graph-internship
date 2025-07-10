import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

class HelperClass:
    def __init__(self):
        self.api_key = api_key
        self.base_url = "https://api.weatherbit.io/v2.0/"

    def takeWeatherHourly(self, hours, city):
       
        if not (1 <= hours <= 120):
            hours = 24 

        try:
            url = f"{self.base_url}forecast/hourly?city={city}&key={self.api_key}&hours={hours}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data

        except Exception as e:
            print(f"An unexpected error occurred in takeWeatherHourly: {e}")
            return {"error": f"Unexpected error: {e}"}

    def takeWeather(self, city):

        try:
            url = f"{self.base_url}current?city={city}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            return data

        except Exception as e:
            print(f"An unexpected error occurred in takeWeather: {e}")
            return {"error": f"Unexpected error: {e}"}

    def takeUserLocation(self):
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        result = requests.get(f"https://ipinfo.io/{ip}/json")
        return result.json()["region"]

 
