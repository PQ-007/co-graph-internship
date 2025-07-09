# app2.py
import streamlit as st
import pandas as pd
import requests

st.title("東京の気象データ可視化")

# Open-Meteo APIからデータ取得
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 35.6895,
    "longitude": 139.6917,
    "hourly": ["temperature_2m", "relative_humidity_2m"],
    "timezone": "Asia/Tokyo"
}
response = requests.get(url, params=params)
data = response.json()

# データフレームに変換
df = pd.DataFrame(data["hourly"])

# 時刻をdatetime型に変換してindexに設定
df["time"] = pd.to_datetime(df["time"])
df.set_index("time", inplace=True)

# 表示
st.line_chart(df["temperature_2m"])
st.line_chart(df["relative_humidity_2m"])