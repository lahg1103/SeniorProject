import requests
from datetime import timedelta
from typing import Literal

# Open-Meteo API Endpoints
WEATHER_FORECAST_URL = "https://open-meteo.com/v1/forecast"
HISTORICAL_WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


class WeatherAPIError(Exception):
    pass

# Geocoding to get latitude and longitude of user's destination


def geocode(destination: str):
    """Get latitude and longitude for a given destination using Open-Meteo Geocoding API."""
    params = {
        "name": destination,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(GEOCODING_URL, params=params)
    if response.status_code != 200:
        raise WeatherAPIError("Failed to fetch geocoding data.")

    data = response.json()
    if not data.get("results"):
        raise WeatherAPIError(
            f"There was no location found for '{destination}'.")

    location = data["results"][0]
    return location["latitude"], location["longitude"], location["name"]


def weather_description(temp_max, temp_min, precipitation):
    """Generate a weather description based on temperature and precipitation."""
    if temp_max is None or temp_min is None:
        return "No weather data available."

    if temp_max <= 5:
        temp_description = "very cold"
    elif temp_max <= 15:
        temp_description = "cool"
    elif temp_max <= 25:
        temp_description = "warm"
    else:
        temp_description = "hot"

    if precipitation is None or precipitation == 0:
        rain_description = "no expected rain"
    elif precipitation < 3:
        rain_description = "light rain"
    else:
        rain_description = "heavy rain"

    return f"The weather will be {temp_description} with {rain_description}."

# Turning raw API data into a normalized format using list for forecast and historical


def normalize_daily(dates, temp_max, temp_min, precipitation, source: Literal["forecast", "historical"]):
    days = []
    for i, d in enumerate(dates):
        days.append({
            "date": d,
            "temp_max": temp_max[i] if temp_max else None,
            "temp_min": temp_min[i] if temp_min else None,
            "precipitation": precipitation[i] if precipitation else None,
            "description": weather_description(
                temp_max[i] if temp_max else None,
                temp_min[i] if temp_min else None,
                precipitation[i] if precipitation else None
            ),
        })
    return {
        "source": source,
        "days": days
    }


def weather_forecast(lat, lon, start_date, end_date):
    """Fetch weather forecast data from Open-Meteo API."""
    params = {
        "latitude": lat,
        "longitude": lon,
       "start_date": start_date.date().isoformat(),
        "end_date": end_date.date().isoformat(),
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    response = requests.get(WEATHER_FORECAST_URL, params=params)
    if response.status_code != 200:
        raise WeatherAPIError("Failed to fetch weather forecast data.")

    data = response.json()
    daily = data.get("daily") or {}
    dates = daily.get("time") or []
    if not dates:
        raise WeatherAPIError(
            "No forecast data available for the specified dates.")

    return normalize_daily(
        dates,
        daily.get("temperature_2m_max", []),
        daily.get("temperature_2m_min", []),
        daily.get("precipitation_sum", []),
        source="forecast"
    )


def historical_weather(lat, lon, start_date, end_date):
    shift_start_date = (start_date - timedelta(days=365))
    shift_end_date = (end_date - timedelta(days=365))

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": shift_start_date.date().isoformat(),
        "end_date": shift_end_date.date().isoformat(),
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    response = requests.get(HISTORICAL_WEATHER_URL, params=params)
    if response.status_code != 200:
        raise WeatherAPIError("Failed to fetch historical weather data.", Exception)

    data = response.json()
    daily = data.get("daily") or {}
    dates = daily.get("time") or []
    if not dates:
        raise WeatherAPIError(
            "No historical data available for the specified dates.")

    return normalize_daily(
        dates,
        daily.get("temperature_2m_max", []),
        daily.get("temperature_2m_min", []),
        daily.get("precipitation_sum", []),
        source="historical"
    )


def get_weather_itinerary(destination, arrival_date, departure_date):
    lat, lon, resolved_name = geocode(destination)

    try:
        weather = weather_forecast(lat, lon, arrival_date, departure_date)
    except WeatherAPIError:
        weather = historical_weather(lat, lon, arrival_date, departure_date)

    weather["location"] = resolved_name
    return weather
