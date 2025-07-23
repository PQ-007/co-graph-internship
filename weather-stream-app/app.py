import streamlit as st
import pandas as pd
from utils.helper_methods import HelperClass
from streamlit_elements import elements, mui, dashboard, nivo

st.set_page_config(layout="wide", page_title="WeatherStream Dashboard", page_icon="🌤️")

# --- Custom CSS for Animations || アニメーション用のカスタムCSS ---
st.markdown("""
    <style>
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        @keyframes shimmer {
            0% { background-position: -200px 0; }
            100% { background-position: 200px 0; }
        }
        .shimmer {
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.03) 50%, transparent 70%);
            background-size: 200px 100%;
            animation: shimmer 4s ease-in-out infinite;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Helper Class || ヘルパークラスの初期化 ---
helper = HelperClass()

# --- Sidebar || サイドバー ---
with st.sidebar:
    user_city_input = st.text_input("🌍 Enter City Name:", key="city_input", placeholder="e.g., Tokyo, London, New York")
    use_current_location = st.checkbox("📍 Auto-detect my location", value=True, key="use_location_checkbox")
    
    st.markdown("### Display Options")
    show_detailed_view = st.checkbox("📊 Detailed Analytics", value=True)
    use_celsius = st.radio("🌡️ Temperature Unit", ["Celsius", "Fahrenheit"], index=0)
    
    st.markdown("### 🔄 Refresh Rate")
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    
    st.markdown("### 📅 Forecast Options")
    show_extended_forecast = st.checkbox("📆 Show 7-Day Forecast", value=True)

# --- Auto-Refresh Logic || 自動更新ロジック ---
if auto_refresh:
    st_autorefresh = st.experimental_rerun
    st_autorefresh(interval=30000)  # Refresh every 30 seconds

# --- Location Detection || 所在地検出 ---
city_to_fetch = None
if use_current_location:
    with st.spinner("🔍 Detecting your location..."):
        try:
            detected_city = helper.take_user_location()
            if detected_city:
                st.sidebar.success(f"📍 **{detected_city}** detected")
                city_to_fetch = detected_city
            else:
                st.sidebar.warning("⚠️ Location detection failed")
                use_current_location = False
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)[:50]}...")
            use_current_location = False
            
if not use_current_location and user_city_input:
    city_to_fetch = user_city_input
elif not use_current_location and not user_city_input:
    st.info("🌟 Enter a city name or enable auto-detection to begin")
    st.stop()

# --- Fetch Weather Data || 気象データの取得 ---
current_data = None
forecast_data = None
weekly_forecast_data = None

if city_to_fetch:
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.spinner(f"🌤️ Fetching weather for **{city_to_fetch}**..."):
            current_data = helper.take_weather(city_to_fetch)
    with col2:
        with st.spinner(f"📈 Loading hourly forecast data..."):
            forecast_data = helper.take_weather_hourly(24, city_to_fetch)
    with col3:
        if show_extended_forecast:
            with st.spinner(f"📅 Loading weekly forecast data..."):
                weekly_forecast_data = helper.take_weather_daily(city_to_fetch)

# --- Dashboard Layout || ダッシュボードのレイアウト ---
layout = [
    dashboard.Item("hero_banner", 0, 0, 12, 3),
    dashboard.Item("main_temp_card", 0, 2, 3, 5),
    dashboard.Item("condition_card", 3, 2, 4, 5),
    dashboard.Item("sun_set_rise", 7, 2, 3, 3),
    dashboard.Item("metrics_card", 7, 2, 3, 8),
    dashboard.Item("hourly_forecast", 0, 6, 7, 6),
    dashboard.Item("weekly_forecast", 0, 12, 12, 3 ),
    dashboard.Item("air_quality", 0, 10, 3, 5),
]

# --- Create Dashboard || ダッシュボードの作成 ---
with elements("weather_dashboard"):
    with dashboard.Grid(layout, rowHeight=60):

        # --- Hero Banner || ヒーローバナー ---
        with mui.Paper(
            key="hero_banner",
            sx={
                "p": 3,
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "height": "100%",
                "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%)",
                "backdropFilter": "blur(20px)",
                "borderRadius": 4,
                "border": "1px solid rgba(255,255,255,0.3)",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.2)",
                "color": "white",
                "position": "relative",
                "overflow": "hidden",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "boxShadow": "0 12px 40px rgba(0,0,0,0.3)",
                }
            }
        ):
            with mui.Box(sx={"position": "absolute", "top": 0, "left": 0, "right": 0, "bottom": 0, "className": "shimmer"}):
                pass
            
            with mui.Box(sx={"zIndex": 1, "position": "relative", "display": "flex", "alignItems": "center", "width": "100%"}):
                if city_to_fetch and current_data and "error" not in current_data and "data" in current_data and current_data["data"]:
                    current_weather = current_data["data"][0]
                    
                    with mui.Box(sx={"flex": 1}):
                        mui.Typography(
                            f"{current_weather.get('city_name', city_to_fetch)}, {current_weather.get('country_code', '')}",
                            variant="h3",
                            sx={"fontWeight": "700", "mb": 1, "textShadow": "2px 2px 6px rgba(0,0,0,0.4)"}
                        )
                        weather_desc = current_weather.get('weather', {}).get('description', 'N/A')
                        mui.Typography(
                            weather_desc,
                            variant="h6",
                            sx={"opacity": 0.9, "fontWeight": "300", "textTransform": "capitalize"}
                        )
                        with mui.Box(sx={"display": "flex", "alignItems": "center", "mt": 1}):
                            mui.Box(sx={
                                "width": 10,
                                "height": 10,
                                "borderRadius": "50%",
                                "backgroundColor": "#00E676",
                                "mr": 1,
                                "animation": "pulse 2s infinite"
                            })
                            mui.Typography("Live Data", variant="caption", sx={"opacity": 0.8, "fontWeight": "400"})
                    
                    with mui.Box(sx={"display": "flex", "justifyContent": "center", "alignItems": "center", "flex": 1}):
                        weather_icon_code = current_weather.get('weather', {}).get('icon', '')
                        if weather_icon_code:
                            mui.Avatar(
                                src=f"https://www.weatherbit.io/static/img/icons/{weather_icon_code}.png",
                                sx={
                                    "width": 120,
                                    "height": 120,
                                    "filter": "drop-shadow(0 6px 12px rgba(0,0,0,0.4))",
                                    "animation": "float 3.5s ease-in-out infinite"
                                }
                            )
                    
                    with mui.Box(sx={"flex": 1, "textAlign": "right"}):
                        current_time = current_weather.get('datetime', 'N/A')
                        mui.Typography(
                            "Current Time",
                            variant="caption",
                            sx={"opacity": 0.8, "display": "block", "fontWeight": "400"}
                        )
                        mui.Typography(
                            current_time,
                            variant="h6",
                            sx={"fontWeight": "600", "mb": 2}
                        )
                        temp = helper.convert_temperature(current_weather.get('temp', 0), use_celsius)
                        status_color = "#00E676" if temp > (15 if use_celsius == "Celsius" else 59) else "#2196F3"
                        status_text = "Comfortable" if temp > (15 if use_celsius == "Celsius" else 59) else "Cool"
                        with mui.Chip(
                            label=status_text,
                            sx={
                                "backgroundColor": status_color,
                                "color": "white",
                                "fontWeight": "bold",
                                "borderRadius": "4px",
                                "padding": "4px 12px"
                            }
                        ):
                            pass
                else:
                    mui.Typography(
                        "🌟 Welcome to WeatherStream",
                        variant="h3",
                        sx={"fontWeight": "700", "textAlign": "center", "width": "100%", "textShadow": "2px 2px 6px rgba(0,0,0,0.4)"}
                    )

        # --- Main Temperature Card　|| メイン温度カード ---
        with mui.Paper(
            key="main_temp_card",
            sx={
                "p": 4,
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
                "height": "100%",
                "borderRadius": 4,
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "color": "white",
                "textAlign": "center",
                "position": "relative",
                "overflow": "hidden",
                "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-5px)",
                    "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                }
            }
        ):
            with mui.Box(sx={
                "position": "absolute",
                "top": "-50px",
                "right": "-50px",
                "width": 150,
                "height": 150,
                "borderRadius": "50%",
                "background": "rgba(255,255,255,0.15)",
                "animation": "float 4s ease-in-out infinite"
            }):
                pass
            
            with mui.Box(sx={"zIndex": 1, "position": "relative"}):
                mui.Typography("Current Temperature", variant="h6", sx={"mb": 2, "opacity": 0.9, "fontWeight": "400"})
                if current_data and "error" not in current_data and "data" in current_data and current_data["data"]:
                    current_weather = current_data["data"][0]
                    temp = helper.convert_temperature(current_weather.get('temp', 0), use_celsius)
                    feels_like = helper.convert_temperature(current_weather.get('app_temp', 0), use_celsius)
                    mui.Typography(
                        f"{temp}°{'C' if use_celsius == 'Celsius' else 'F'}",
                        variant="h1",
                        sx={"fontWeight": "100", "fontSize": "4.5rem", "mb": 1, "textShadow": "2px 2px 6px rgba(0,0,0,0.4)"}
                    )
                    mui.Typography(
                        f"Feels like {feels_like}°{'C' if use_celsius == 'Celsius' else 'F'}",
                        variant="h6",
                        sx={"opacity": 0.8, "fontWeight": "300", "mb": 2}
                    )
                    with mui.Box(sx={"display": "flex", "alignItems": "center", "justifyContent": "center", "gap": 1}):
                        mui.Typography("📈", variant="h6")
                        mui.Typography("Trending", variant="body2", sx={"opacity": 0.8})
                else:
                    mui.Typography(f"--°{'C' if use_celsius == 'Celsius' else 'F'}", variant="h1", sx={"fontWeight": "100", "fontSize": "4.5rem"})
                    mui.Typography("No data available", variant="body2", sx={"opacity": 0.8})

        # --- Condition Card || コンディションカード ---
        with mui.Paper(
            key="condition_card",
            sx={
                "p": 3,
                "display": "flex",
                "flexDirection": "column",
                "height": "100%",
                "borderRadius": 4,
                "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%)",
                "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255,255,255,0.3)",
                "color": "white",
                "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-5px)",
                    "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                }
            }
        ):
            mui.Typography("Weather Conditions", variant="h6", sx={"mb": 3, "fontWeight": "600"})
            if current_data and "error" not in current_data and "data" in current_data and current_data["data"]:
                current_weather = current_data["data"][0]
                humidity = current_weather.get('rh', 0)
                with mui.Box(sx={"mb": 2}):
                    with mui.Box(sx={"display": "flex", "justifyContent": "space-between", "mb": 1}):
                        mui.Typography("💧 Humidity", variant="body2")
                        mui.Typography(f"{humidity}%", variant="body2", sx={"fontWeight": "bold"})
                    mui.LinearProgress(
                        variant="determinate",
                        value=humidity if isinstance(humidity, (int, float)) else 0,
                        sx={
                            "height": 10,
                            "borderRadius": 2,
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "& .MuiLinearProgress-bar": {
                                "backgroundColor": "#2196F3",
                                "borderRadius": 2
                            }
                        }
                    )
                clouds = current_weather.get('clouds', 0)
                with mui.Box(sx={"mb": 2}):
                    with mui.Box(sx={"display": "flex", "justifyContent": "space-between", "mb": 1}):
                        mui.Typography("☁️ Cloud Coverage", variant="body2")
                        mui.Typography(f"{clouds}%", variant="body2", sx={"fontWeight": "bold"})
                    mui.LinearProgress(
                        variant="determinate",
                        value=clouds if isinstance(clouds, (int, float)) else 0,
                        sx={
                            "height": 10,
                            "borderRadius": 2,
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "& .MuiLinearProgress-bar": {
                                "backgroundColor": "#9E9E9E",
                                "borderRadius": 2
                            }
                        }
                    )
                uv_value = current_weather.get('uv', 0)
                uv_color = "#00E676" if uv_value < 3 else "#FF9800" if uv_value < 6 else "#F44336"
                with mui.Box(sx={"mb": 2}):
                    with mui.Box(sx={"display": "flex", "justifyContent": "space-between", "mb": 1}):
                        mui.Typography("☀️ UV Index", variant="body2")
                        mui.Typography(str(uv_value), variant="body2", sx={"fontWeight": "bold", "color": uv_color})
                    mui.LinearProgress(
                        variant="determinate",
                        value=(uv_value / 11) * 100 if isinstance(uv_value, (int, float)) else 0,
                        sx={
                            "height": 10,
                            "borderRadius": 2,
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "& .MuiLinearProgress-bar": {
                                "backgroundColor": uv_color,
                                "borderRadius": 2
                            }
                        }
                    )
                visibility = current_weather.get('vis', 0)
                with mui.Box(sx={"mb": 2}):
                    with mui.Box(sx={"display": "flex", "justifyContent": "space-between", "mb": 1}):
                        mui.Typography("👁️ Visibility", variant="body2")
                        mui.Typography(
                            f"{visibility:.1f} km" if isinstance(visibility, (int, float)) else "N/A",
                            variant="body2",
                            sx={"fontWeight": "bold"}
                        )
                    vis_percentage = min((visibility / 10) * 100, 100) if isinstance(visibility, (int, float)) else 0
                    mui.LinearProgress(
                        variant="determinate",
                        value=vis_percentage,
                        sx={
                            "height": 10,
                            "borderRadius": 2,
                            "backgroundColor": "rgba(255,255,255,0.2)",
                            "& .MuiLinearProgress-bar": {
                                "backgroundColor": "#00BCD4",
                                "borderRadius": 2
                            }
                        }
                    )
            else:
                mui.Typography("No weather data available", variant="body2", sx={"opacity": 0.8})
       
       # --- Sunset and rise Card　|| 日の出と日の入りカード ---
        with mui.Paper(
            key="sun_set_rise",
            sx={
                "p": 3,
                "display": "flex",
                "flexDirection": "column",
                "height": "100%",
                "borderRadius": 4,
                "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%)",
                "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255,255,255,0.3)",
                "color": "white",
                "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-5px)",
                    "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                }
            }
        ):
            mui.Typography("Sunrise and Sunset", variant="h6", sx={"mb": 2, "fontWeight": "600", "textAlign": "center"})
            if current_data and "error" not in current_data and "data" in current_data and current_data["data"]:
                current_weather = current_data["data"][0]
                sunrise = current_weather.get('sunrise', 'N/A')
                sunset = current_weather.get('sunset', 'N/A')

                # Format sunrise/sunset times (assuming they are in HH:MM format)
                try:
                    sunrise_formatted = pd.to_datetime(sunrise, format='%H:%M').strftime('%I:%M %p') if sunrise != 'N/A' else 'N/A'
                    sunset_formatted = pd.to_datetime(sunset, format='%H:%M').strftime('%I:%M %p') if sunset != 'N/A' else 'N/A'
                except ValueError:
                    sunrise_formatted = sunrise
                    sunset_formatted = sunset

                with mui.Box(sx={
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "width": "100%",
                    "gap": 2,
                    "@media (max-width: 600px)": {
                        "flexDirection": "column",
                        "gap": 1
                    }
                }):
                    # Sunrise Section
                    with mui.Box(sx={
                        "textAlign": "center",
                        "flex": 1,
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "p": 1,
                        "borderRadius": 2,
                        "background": "rgba(255, 255, 255, 0.1)",
                        "transition": "background 0.3s ease",
                        "&:hover": {
                            "background": "rgba(255, 255, 255, 0.2)",
                        }
                    }):
                        
                        mui.Typography("Sunrise", variant="subtitle2", sx={"mb": 0.5, "opacity": 0.8})
                        mui.Typography(sunrise_formatted, variant="h6", sx={"fontWeight": "bold"})

                    # Sunset Section
                    with mui.Box(sx={
                        "textAlign": "center",
                        "flex": 1,
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "p": 1,
                        "borderRadius": 2,
                        "background": "rgba(255, 255, 255, 0.1)",
                        "transition": "background 0.3s ease",
                        "&:hover": {
                            "background": "rgba(255, 255, 255, 0.2)",
                        }
                    }):     
                        mui.Typography("Sunset", variant="subtitle2", sx={"mb": 0.5, "opacity": 0.8})
                        mui.Typography(sunset_formatted, variant="h6", sx={"fontWeight": "bold"})
            else:
                mui.Typography(
                    "No sunrise/sunset data available",
                    variant="body2",
                    sx={"opacity": 0.8, "textAlign": "center", "py": 2}
                )           
        
        # --- Metrics Card || メトリクスカード ---
        with mui.Paper(
            key="metrics_card",
            sx={
                "p": 3,
                "display": "flex",
                "flexDirection": "column",
                "height": "100%",
                "borderRadius": 4,
                "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%)",
                "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255,255,255,0.3)",
                "color": "white",
                "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-5px)",
                    "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                }
            }
        ):
            mui.Typography("Atmospheric Data", variant="h6", sx={"mb": 3, "fontWeight": "600", "textAlign": "center"})
            if current_data and "error" not in current_data and "data" in current_data and current_data["data"]:
                current_weather = current_data["data"][0]
                wind_speed = current_weather.get('wind_spd', 0)
                wind_dir = current_weather.get('wind_cdir_full', 'N/A')
                with mui.Box(sx={"mb": 3, "textAlign": "center"}):
                    mui.Typography("🌪️ Wind", variant="subtitle2", sx={"mb": 1, "opacity": 0.8})
                    mui.Typography(
                        f"{wind_speed:.1f} m/s" if isinstance(wind_speed, (int, float)) else "N/A",
                        variant="h4",
                        sx={"fontWeight": "bold", "mb": 0.5}
                    )
                    mui.Typography(wind_dir, variant="body2", sx={"opacity": 0.8})
                pressure = current_weather.get('pres', 0)
                with mui.Box(sx={"mb": 3, "textAlign": "center"}):
                    mui.Typography("🌡️ Pressure", variant="subtitle2", sx={"mb": 1, "opacity": 0.8})
                    mui.Typography(
                        f"{pressure:.0f} mb" if isinstance(pressure, (int, float)) else "N/A",
                        variant="h4",
                        sx={"fontWeight": "bold", "mb": 0.5}
                    )
                    mui.Typography("📈 Steady", variant="body2", sx={"opacity": 0.8})
                dew_point = helper.convert_temperature(current_weather.get('dewpt', 0), use_celsius)
                with mui.Box(sx={"mb": 2, "textAlign": "center"}):
                    mui.Typography("💧 Dew Point", variant="subtitle2", sx={"mb": 1, "opacity": 0.8})
                    mui.Typography(
                        f"{dew_point}°{'C' if use_celsius == 'Celsius' else 'F'}" if isinstance(dew_point, (int, float)) else "N/A",
                        variant="h4",
                        sx={"fontWeight": "bold"}
                    )
                with mui.Box(sx={"mt": 2, "textAlign": "center"}):
                    mui.Typography("🌬️ Air Quality", variant="subtitle2", sx={"mb": 1, "opacity": 0.8})
                    with mui.Chip(
                        label="Good",
                        sx={
                            "backgroundColor": "#00E676",
                            "color": "white",
                            "fontWeight": "bold",
                            "borderRadius": "4px",
                            "padding": "4px 12px"
                        }
                    ):
                        pass
            else:
                mui.Typography("No atmospheric data available", variant="body2", sx={"opacity": 0.8})

        # --- Hourly Forecast　|| 時間別予報 ---
        with mui.Paper(
            key="hourly_forecast",
            sx={
                "p": 3,
                "display": "flex",
                "flexDirection": "column",
                "height": "100%",
                "borderRadius": 4,
                "background": "gray",
                "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255,255,255,0.3)",
                "color": "white",
                "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                "transition": "all 0.3s ease",
                "&:hover": {
                    "transform": "translateY(-5px)",
                    "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                }
            }
        ):
            mui.Typography("24-Hour Forecast", variant="h6", sx={"mb": 2, "fontWeight": "600"})
            if forecast_data and "error" not in forecast_data and "data" in forecast_data and forecast_data["data"]:
                forecast_list = forecast_data["data"][:16]
                temp_data = []
                for i, hour_data in enumerate(forecast_list):
                    time_str = hour_data.get('timestamp_local', '')
                    if time_str:
                        try:
                            hour = pd.to_datetime(time_str).strftime('%H:%M')
                        except:
                            hour = f"H{i+1}"
                    else:
                        hour = f"H{i+1}"
                    temp_data.append({"x": hour, "y": helper.convert_temperature(hour_data.get('temp', 0), use_celsius)})
                chart_data = [
                    {"id": f"Temperature (°{'C' if use_celsius == 'Celsius' else 'F'})", "data": temp_data},
                ]
                with mui.Box(sx={"height": "300px", "width": "100%"}):
                    nivo.Line(
                        data=chart_data,
                        margin={"top": 20, "right": 50, "bottom": 60, "left": 60},
                        xScale={"type": "point"},
                        yScale={"type": "linear", "min": "auto", "max": "auto"},
                        curve="cardinal",
                        axisTop=None,
                        axisRight=None,
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": -45,
                            "tickColor": "#ffffff",
                            "legendColor": "#ffffff",
                            "legend": "Time",
                            "legendOffset": 45,
                            "legendPosition": "middle"
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "Temp",
                            "legendOffset": -50,
                            "legendPosition": "middle"
                        },
                        pointSize=10,
                        pointColor={"theme": "background"},
                        pointBorderWidth=2,
                        pointBorderColor={"from": "serieColor"},
                        pointLabelYOffset=-12,
                        useMesh=True,
                        enableGridX=False,
                        enableGridY=True,
                        gridYValues=5,
                        colors=["#2196F3"],
                        lineWidth=3,
                        animate=True,
                        motionConfig="gentle"
                    )
            else:
                mui.Typography("No hourly forecast data available", variant="body2", sx={"opacity": 0.8})

        # --- Weekly Forecast　|| 週間予報 ---
        with mui.Paper(
                key="weekly_forecast",
                sx={
                    "p": 3,
                    "display": "flex",
                    "flexDirection": "column",
                    "height": "100%",
                    "borderRadius": 4,
                    "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%)",
                    "backdropFilter": "blur(20px)",
                    "border": "1px solid rgba(255,255,255,0.3)",
                    "color": "white",
                    "boxShadow": "0 12px 24px rgba(0,0,0,0.15)",
                    "transition": "all 0.3s ease",
                    "&:hover": {
                        "transform": "translateY(-5px)",
                        "boxShadow": "0 16px 32px rgba(0,0,0,0.2)",
                    }
                }
            ):
                mui.Typography("7-Day Forecast", variant="h6", sx={"mb": 2, "fontWeight": "600", "textAlign": "center"})
                if weekly_forecast_data and "error" not in weekly_forecast_data and "data" in weekly_forecast_data and weekly_forecast_data["data"]:
                    forecast_list = weekly_forecast_data["data"][:7]
                    temp_data = []
                    precip_data = []
                    labels = []
                    icons = []
                    temps = []

                    for i, day_data in enumerate(forecast_list):
                        date_str = day_data.get('datetime', '')
                        if date_str:
                            try:
                                day = pd.to_datetime(date_str).strftime('%a')
                            except ValueError:
                                day = f"Day {i+1}"
                        else:
                            day = f"Day {i+1}"
                        labels.append(day)
                        temp = helper.convert_temperature(day_data.get('temp', 0), use_celsius)
                        temp_data.append(temp)
                        precip_data.append(day_data.get('precip', 0))
                        temps.append(f"{temp:.1f}°{'C' if use_celsius == 'Celsius' else 'F'}" if isinstance(temp, (int, float)) else "N/A")
                        icon_code = day_data.get('weather', {}).get('icon', '')
                        icons.append(f"https://www.weatherbit.io/static/img/icons/{icon_code}.png" if icon_code else None)

                    # Display icons, days, and temperatures above the chart
                    with mui.Box(sx={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "mb": 2,
                        "flexWrap": "wrap",
                        "@media (max-width: 600px)": {
                            "flexDirection": "column",
                            "gap": 1.5,
                            "alignItems": "center"
                        }
                    }):
                        for i, (day, icon_url, temp) in enumerate(zip(labels, icons, temps)):
                            with mui.Box(sx={
                                "textAlign": "center",
                                "flex": "1 0 12%",
                                "minWidth": "70px",
                                "p": 1,
                                "borderRadius": 2,
                                
                                "transition": "background 0.3s ease",
                                "&:hover": {
                                    "background": "rgba(255, 255, 255, 0.2)",
                                }
                            }):
                                if icon_url:
                                    mui.Avatar(
                                        src=icon_url,
                                        sx={"width": 30, "height": 30, "mx": "auto", "mb": 0.5},
                                        ariaLabel=f"Weather icon for {day}"
                                    )
                                mui.Typography(day, variant="caption", sx={"opacity": 0.8, "mb": 0.5})
                                mui.Typography(temp, variant="body2", sx={"fontWeight": "bold", "color": "#00E676"})