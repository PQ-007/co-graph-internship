import streamlit as st
import pandas as pd
import numpy as np
from utils.helper_methods import HelperClass 

st.title("Today's Weather & Hourly Forecast")
st.set_page_config(layout="wide")

# city_name = st.text_input(label="Type City name", placeholder="City name")

helper = HelperClass()
city = helper.takeUserLocation()


current_data = helper.takeWeather(city)

if current_data and "error" not in current_data:
    if 'data' in current_data and len(current_data['data']) > 0:
        current_weather = current_data['data'][0]

        st.header(f"Current Conditions in {current_weather.get('city_name', 'N/A')}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Temperature", f"{current_weather.get('temp', 'N/A')} °C",
                      delta=f"{current_weather.get('app_temp', 'N/A')} °C (Feels like)")
        with col2:
            st.metric("Description", current_weather['weather'].get('description', 'N/A'))
        with col3:
            st.metric("Humidity", f"{current_weather.get('rh', 'N/A')}%")
        with col4:
            st.metric("Wind Speed", f"{current_weather.get('wind_spd', 'N/A')} m/s")
    else:
        st.warning("No current weather data found for this city. Please check the city name or try again.")
elif current_data and "error" in current_data:
    st.error(f"Error fetching current weather data: {current_data['error']}")
    if 'details' in current_data:
        st.json(current_data['details'])
else:
    st.error("Failed to retrieve current weather data. Check network or API key.")

st.header("Hourly Weather Forecast")
forecast_data = helper.takeWeatherHourly(24, city)

if forecast_data and "error" not in forecast_data:
        if 'data' in forecast_data and len(forecast_data['data']) > 0:
            df_forecast = pd.DataFrame(forecast_data['data'])

            df_forecast['timestamp_local'] = pd.to_datetime(df_forecast['timestamp_local'])
            df_forecast = df_forecast.set_index('timestamp_local')

            chart_columns = ['temp']
            available_chart_columns = []
            for col in chart_columns:
                if col in df_forecast.columns:
                    df_forecast[col] = pd.to_numeric(df_forecast[col], errors='coerce')
                    if not df_forecast[col].isnull().all(): 
                        available_chart_columns.append(col)

            if available_chart_columns:
                st.subheader(f"Hourly Trends for {city}")
                st.area_chart(df_forecast[available_chart_columns], use_container_width=True)
                st.caption("Hover over the chart to see hourly details.")

                with st.expander("View Raw Hourly Forecast Data"):
                    st.dataframe(df_forecast)
            else:
                st.warning("No suitable numerical data found for hourly forecast charts.")

       