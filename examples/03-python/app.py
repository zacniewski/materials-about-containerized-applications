#!/usr/bin/env python3
"""
Simple Python client querying Open‑Meteo for Gdynia current weather and forecast.
Requirements:
- Uses the 'requests' package to call the API.
- Prints current conditions and next 24h hourly forecast.

Usage (locally):
  python app.py

Usage (Docker):
  docker build -t meteo-gdynia:latest .
  docker run --rm meteo-gdynia:latest
"""
import datetime as dt
import os
import sys
import requests

# Coordinates for Gdynia, Poland
LAT = float(os.getenv("LAT", "54.5189"))
LON = float(os.getenv("LON", "18.5319"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Warsaw")
HOURS_AHEAD = int(os.getenv("HOURS_AHEAD", "24"))

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# We will request current weather and hourly forecast for a few key variables
PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
    ],
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
    ],
    "timezone": TIMEZONE,
}


def fetch_weather():
    try:
        # Open‑Meteo accepts arrays but also comma-separated strings; requests will handle list->multi-values.
        resp = requests.get(BASE_URL, params=PARAMS, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"HTTP error while calling Open-Meteo: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Could not parse JSON from Open-Meteo: {e}", file=sys.stderr)
        sys.exit(2)


def print_current(data: dict):
    current = data.get("current", {})
    if not current:
        print("Brak danych bieżących (current).")
        return

    t = current.get("time")
    temp = current.get("temperature_2m")
    rh = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")

    print("=== Pogoda bieżąca: Gdynia ===")
    print(f"Czas: {t}")
    print(f"Temperatura: {temp} °C")
    print(f"Wilgotność względna: {rh} %")
    print(f"Prędkość wiatru: {wind} m/s")
    print()


def print_hourly_forecast(data: dict, hours_ahead: int = 24):
    hourly = data.get("hourly", {})
    times = hourly.get("time") or []
    temps = hourly.get("temperature_2m") or []
    rhs = hourly.get("relative_humidity_2m") or []
    winds = hourly.get("wind_speed_10m") or []

    if not times:
        print("Brak danych prognostycznych (hourly).")
        return

    print(f"=== Prognoza godzinowa (kolejne {hours_ahead} h): Gdynia ===")

    # Determine index range for the next hours starting from now
    now = dt.datetime.now().replace(minute=0, second=0, microsecond=0)
    # Times are strings in ISO format in the provided timezone
    def parse_time(s):
        try:
            return dt.datetime.fromisoformat(s)
        except Exception:
            return None

    parsed_times = [parse_time(t) for t in times]

    # Find first index >= now
    start_idx = 0
    for i, t in enumerate(parsed_times):
        if t and t >= now:
            start_idx = i
            break

    end_idx = min(start_idx + hours_ahead, len(times))

    for i in range(start_idx, end_idx):
        t = times[i]
        temp = temps[i] if i < len(temps) else None
        rh = rhs[i] if i < len(rhs) else None
        wind = winds[i] if i < len(winds) else None
        print(f"- {t}: {temp} °C, RH {rh} %, wiatr {wind} m/s")


if __name__ == "__main__":
    data = fetch_weather()
    print_current(data)
    print_hourly_forecast(data, HOURS_AHEAD)
