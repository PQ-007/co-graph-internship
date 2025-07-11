import requests
from dotenv import load_dotenv
import os
import streamlit as st
import time
from streamlit_elements import elements, html
import base64

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

class HelperClass:
    def __init__(self):
        self.api_key = api_key
        self.base_url = "https://api.weatherbit.io/v2.0/"

    def take_weather_hourly(self, hours, city):
       
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

    def take_weather(self, city):

        try:
            url = f"{self.base_url}current?city={city}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            return data

        except Exception as e:
            print(f"An unexpected error occurred in takeWeather: {e}")
            return {"error": f"Unexpected error: {e}"}

    def take_user_location(self):
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        result = requests.get(f"https://ipinfo.io/{ip}/json")
        return result.json()["region"]

    def stream_header_text(self, text: str, speed: float = 0.05):

        title_placeholder = st.empty()
        current_title = ""
        for char in text:
            current_title += char
            title_placeholder.header(current_title) 
            time.sleep(speed)

    def stream_sub_header_text(self, text: str, speed: float = 0.05):

        title_placeholder = st.empty()
        current_title = ""
        for char in text:
            current_title += char
            title_placeholder.subheader(current_title) 
            time.sleep(speed)

    def display_animeted_icon_on_elements(self, path_or_url):
        with elements("animated_icon_container"):
            if path_or_url.startswith("http"):
                html.img(src=path_or_url, style={"width": "100%", "height": "auto"})
            else:
                try:
                    with open(path_or_url, "rb") as file:
                        contents = file.read()
                        data_url = base64.b64encode(contents).decode("utf-8")
                        html.img(src=f"data:image/gif;base64,{data_url}", style={"width": "100%", "height": "auto"})
                except FileNotFoundError:
                    html.div("GIF file not found.")
