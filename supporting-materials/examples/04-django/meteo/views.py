import asyncio
from typing import Any, Dict, List, Optional

import httpx
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import CityQueryForm

GEOCODE_ENDPOINT = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_ENDPOINT = "https://api.open-meteo.com/v1/forecast"


async def fetch_city(client: httpx.AsyncClient, name: str) -> Dict[str, Any]:
    params = {"name": name.strip(), "count": 1, "language": "pl", "format": "json"}
    r = await client.get(GEOCODE_ENDPOINT, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return {"query": name, "error": "Nie znaleziono miejscowości"}
    res = data["results"][0]
    return {
        "query": name,
        "name": res.get("name"),
        "country": res.get("country"),
        "admin1": res.get("admin1"),
        "lat": res.get("latitude"),
        "lon": res.get("longitude"),
    }


async def fetch_weather(client: httpx.AsyncClient, lat: float, lon: float, hours: int = 12) -> Dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "forecast_hours": max(0, min(hours, 72)),
        "timezone": "auto",
    }
    r = await client.get(FORECAST_ENDPOINT, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


async def query_cities(cities: List[str], hours: int) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    async with httpx.AsyncClient(headers={"User-Agent": "meteo-django-example"}) as client:
        geos = await asyncio.gather(*[fetch_city(client, c) for c in cities], return_exceptions=True)
        for geo in geos:
            if isinstance(geo, Exception):
                results.append({"error": f"Błąd geokodowania: {geo}"})
                continue
            if geo.get("error"):
                results.append({"query": geo.get("query"), "error": geo.get("error")})
                continue
            try:
                weather = await fetch_weather(client, geo["lat"], geo["lon"], hours)
            except Exception as e:
                results.append({"query": geo.get("query"), "geo": geo, "error": f"Błąd pobierania pogody: {e}"})
                continue
            # Prepare hourly rows for template convenience
            hourly = (weather or {}).get("hourly") or {}
            times = hourly.get("time") or []
            temps = hourly.get("temperature_2m") or []
            hums = hourly.get("relative_humidity_2m") or []
            prec = hourly.get("precipitation") or []
            winds = hourly.get("wind_speed_10m") or []
            n = min(len(times), len(temps), len(hums), len(prec), len(winds))
            if hours:
                n = min(n, hours)
            hourly_rows = [
                {
                    "time": times[i],
                    "temperature_2m": temps[i],
                    "relative_humidity_2m": hums[i],
                    "precipitation": prec[i],
                    "wind_speed_10m": winds[i],
                }
                for i in range(n)
            ]
            results.append({"query": geo.get("query"), "geo": geo, "weather": weather, "hourly_rows": hourly_rows})
    return results


def index(request: HttpRequest) -> HttpResponse:
    form = CityQueryForm(request.GET or None)
    context: Dict[str, Any] = {"form": form, "results": None}
    if form.is_valid():
        cities_raw = form.cleaned_data["cities"]
        hours = form.cleaned_data.get("include_forecast_hours") or 0
        cities = [c.strip() for c in cities_raw.split(",") if c.strip()]
        if cities:
            try:
                results = asyncio.run(query_cities(cities, hours))
            except RuntimeError:
                # If already inside an event loop (rare on dev server), fallback
                results = asyncio.get_event_loop().run_until_complete(query_cities(cities, hours))
            context["results"] = results
    return render(request, "meteo/index.html", context)
