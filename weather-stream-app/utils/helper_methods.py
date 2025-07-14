
import requests
from dotenv import load_dotenv
import os
import streamlit as st
import time
from streamlit_elements import elements, html
import base64

# 環境変数を読み込む
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

class HelperClass:
    def __init__(self):
        # WeatherBit APIキーとベースURLを初期化
        self.api_key = api_key
        self.base_url = "https://api.weatherbit.io/v2.0/"

    def take_weather_hourly(self, hours, city):
        """指定都市の時間ごとの天気予報を取得"""
        if not (1 <= hours <= 120):
            hours = 24  # デフォルト24時間

        try:
            url = f"{self.base_url}forecast/hourly?city={city}&key={self.api_key}&hours={hours}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # エラー時にログとエラー情報を返す
            print(f"時間ごとの天気取得エラー: {e}")
            return {"error": f"エラー: {e}"}

    def take_weather(self, city):
        """指定都市の現在の天気を取得"""
        try:
            url = f"{self.base_url}current?city={city}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # エラー時にログとエラー情報を返す
            print(f"現在の天気取得エラー: {e}")
            return {"error": f"エラー: {e}"}

    def take_weather_daily(self, city):
        """指定都市の日ごとの天気予報を取得"""
        try:
            url = f"{self.base_url}forecast/daily?city={city}&key={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # エラー時にログとエラー情報を返す
            print(f"日ごとの天気取得エラー: {e}")
            return {"error": f"エラー: {e}"}

    def take_user_location(self):
        """IPアドレスからユーザーの地域を検出"""
        try:
            ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
            result = requests.get(f"https://ipinfo.io/{ip}/json")
            return result.json().get("region", None)
        except Exception as e:
            # エラー時にログとNoneを返す
            print(f"現在地検出エラー: {e}")
            return None

    def convert_temperature(self, temp, to_unit="Celsius"):
        """温度を摂氏/華氏に変換"""
        try:
            temp = float(temp)
            if to_unit == "Fahrenheit":
                return round((temp * 9/5) + 32, 1)  # 摂氏→華氏
            return round(temp, 1)  # 摂氏を返す
        except (TypeError, ValueError) as e:
            # エラー時にログと元の値を返す
            print(f"温度変換エラー: {e}")
            return temp

    def stream_header_text(self, text: str, speed: float = 0.05):
        """テキストをヘッダーとして1文字ずつ表示"""
        title_placeholder = st.empty()
        current_title = ""
        for char in text:
            current_title += char
            title_placeholder.header(current_title)
            time.sleep(speed)

    def stream_sub_header_text(self, text: str, speed: float = 0.05):
        """テキストをサブヘッダーとして1文字ずつ表示"""
        title_placeholder = st.empty()
        current_title = ""
        for char in text:
            current_title += char
            title_placeholder.subheader(current_title)
            time.sleep(speed)

    def display_animated_icon_on_elements(self, path_or_url):
        """GIFアイコンをURLまたはローカルファイルから表示"""
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
                    html.div("GIFファイルが見つかりません。")
