import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
from utils.helper_methods import HelperClass
from streamlit_elements import elements, mui, dashboard
from streamlit_elements import nivo
st.set_page_config(layout="wide")
helper = HelperClass()

#
city = helper.takeUserLocation()

# Fetch current weather data
current_data = None
if city:
    with st.spinner(f"Fetching current weather for {city}..."):
        current_data = helper.takeWeather(city)
else:
    st.info("Enter a city name to get weather information.")

# Fetch hourly forecast data
forecast_data = None
if city:
    with st.spinner(f"Fetching hourly forecast for {city}..."):
        forecast_data = helper.takeWeatherHourly(24, city)

# Define the dashboard layout
# Item dimensions are in grid units. Adjust as needed.
# For example, a 4-column grid (total width 12) could have items of width 3.
layout = [
    dashboard.Item("brief banner", 0, 0, 10, 1),
    # Current Weather Card
    dashboard.Item("current_weather_card", 0, 2, 7, 3), # x, y, width, height
    # Hourly Forecast Chart
    dashboard.Item("hourly_forecast_chart", 7, 2, 3, 3),
]

# Create the dashboard
with elements("dashboard"):
    # The Grid component allows you to create a draggable and resizable dashboard
    # You can pass a callback to onLayoutChange to save the layout
    with dashboard.Grid(layout, onLayoutChange=lambda l: print(l)): # Placeholder for layout change handler
        # Card for Current Weather Conditions
        with mui.Paper(key="brief banner", sx={"p": 2, "display": "flex", "flexDirection": "column", "height": "100%", "overflow": "auto", "borderRadius": 2}):
            # helper.streamHeaderText("Welcome to WeatherStream!", speed=0.05)
            with elements("nivo_charts"):

                # Streamlit Elements includes 45 dataviz components powered by Nivo.

                

                DATA = [
                    { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
                    { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
                    { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
                    { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
                    { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
                ]

                with mui.Box(sx={"height": 500}):
                    nivo.Radar(
                        data=DATA,
                        keys=[ "chardonay", "carmenere", "syrah" ],
                        indexBy="taste",
                        valueFormat=">-.2f",
                        margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                        borderColor={ "from": "color" },
                        gridLabelOffset=36,
                        dotSize=10,
                        dotColor={ "theme": "background" },
                        dotBorderWidth=2,
                        motionConfig="wobbly",
                        legends=[
                            {
                                "anchor": "top-left",
                                "direction": "column",
                                "translateX": -50,
                                "translateY": -40,
                                "itemWidth": 80,
                                "itemHeight": 20,
                                "itemTextColor": "#999",
                                "symbolSize": 12,
                                "symbolShape": "circle",
                                "effects": [
                                    {
                                        "on": "hover",
                                        "style": {
                                            "itemTextColor": "#000"
                                        }
                                    }
                                ]
                            }
                        ],
                        theme={
                            "background": "#FFFFFF",
                            "textColor": "#31333F",
                            "tooltip": {
                                "container": {
                                    "background": "#FFFFFF",
                                    "color": "#31333F",
                                }
                            }
                        }
                    )

        with mui.Paper(key="current_weather_card", sx={"p": 2, "display": "flex", "flexDirection": "column", "height": "100%", "overflow": "auto", "borderRadius": 2}):
            st.subheader("Current Weather Conditions")
            if current_data and "error" not in current_data:
                if 'data' in current_data and len(current_data['data']) > 0:
                    current_weather = current_data['data'][0]

                    st.markdown(f"**City:** {current_weather.get('city_name', 'N/A')}, {current_weather.get('country_code', 'N/A')}")
                    st.markdown(f"**Local Time:** {current_weather.get('datetime', 'N/A')}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Temperature", f"{current_weather.get('temp', 'N/A')} °C",
                                  delta=f"{current_weather.get('app_temp', 'N/A')} °C (Feels like)")
                        st.metric("Humidity", f"{current_weather.get('rh', 'N/A')}%")
                        st.metric("Pressure", f"{current_weather.get('pres', 'N/A')} mb")
                    with col2:
                        st.metric("Description", current_weather['weather'].get('description', 'N/A'))
                        st.metric("Wind Speed", f"{current_weather.get('wind_spd', 'N/A')} m/s")
                        st.metric("Visibility", f"{current_weather.get('vis', 'N/A')} km")
                else:
                    st.warning("No current weather data found for this city. Please check the city name or try again.")
            elif current_data and "error" in current_data:
                st.error(f"Error fetching current weather data: {current_data['error']}")
                if 'details' in current_data:
                    st.json(current_data['details'])
            elif city: # Only show this if a city was typed but no data was fetched
                st.info("Enter a city name to fetch current weather data.")


        # Card for Hourly Weather Forecast
        with mui.Paper(key="hourly_forecast_chart", sx={"p": 2, "display": "flex", "flexDirection": "column", "height": "100%", "overflow": "auto", "borderRadius": 2}):
            st.subheader("Hourly Weather Forecast")
            if forecast_data and "error" not in forecast_data:
                if 'data' in forecast_data and len(forecast_data['data']) > 0:
                    df_forecast = pd.DataFrame(forecast_data['data'])

                    # Convert timestamp to datetime and set as index for charting
                    df_forecast['timestamp_local'] = pd.to_datetime(df_forecast['timestamp_local'])
                    df_forecast = df_forecast.set_index('timestamp_local')

                    # Select relevant columns for charting and ensure they are numeric
                    chart_columns = ['temp', 'app_temp', 'rh', 'wind_spd']
                    available_chart_columns = []
                    for col in chart_columns:
                        if col in df_forecast.columns:
                            df_forecast[col] = pd.to_numeric(df_forecast[col], errors='coerce')
                            # Only add if there's actual non-null numeric data
                            if not df_forecast[col].isnull().all():
                                available_chart_columns.append(col)

                    if available_chart_columns:
                        st.line_chart(df_forecast[available_chart_columns], use_container_width=True)
                        st.caption("Hover over the chart to see hourly details.")

                        with st.expander("View Raw Hourly Forecast Data"):
                            st.dataframe(df_forecast)
                    else:
                        st.warning("No suitable numerical data found for hourly forecast charts.")
                else:
                    st.warning("No hourly forecast data found for this city. Please check the city name or try again.")
            elif forecast_data and "error" in forecast_data:
                st.error(f"Error fetching hourly forecast data: {forecast_data['error']}")
                if 'details' in forecast_data:
                    st.json(forecast_data['details'])
            elif city: 
                st.info("Enter a city name to fetch hourly forecast data.")

