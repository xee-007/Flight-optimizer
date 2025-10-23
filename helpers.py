from __future__ import annotations
import requests
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
from config import config

# ---------- City Resolution ----------
def resolve_city_code(city_name: str) -> Tuple[str, str]:
    """Convert city name (e.g., London) → Kiwi metropolitan code (e.g., LON)."""
    url = f"{config.TEQUILA_BASE}/locations/query"
    headers = {
        "apikey": config.KIWI_API_KEY,
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }
    params = {
        "term": city_name,
        "location_types": "city",
        "limit": 1,
        "active_only": "true",
        "locale": "en-US",
        "sort": "rank",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json().get("locations", [])
    if not data:
        raise ValueError(f"Could not resolve city '{city_name}'")
    city = data[0]
    return city["code"], city.get("name", city_name)

# ---------- Date Helper ----------
def next_24h_date_range_utc(now: Optional[datetime] = None) -> Tuple[str, str]:
    """Return (date_from, date_to) formatted for Kiwi API."""
    now = now or datetime.utcnow()
    today = now.date()
    tomorrow = today + timedelta(days=1)
    return today.strftime("%d/%m/%Y"), tomorrow.strftime("%d/%m/%Y")

# ---------- Flight Logic ----------
def search_cheapest_oneway(origin_code: str, dest_code: str, currency: str = config.DEFAULT_CURRENCY) -> Optional[Dict[str, Any]]:
    """Return cheapest one-way flight in next 24h."""
    date_from, date_to = next_24h_date_range_utc()
    url = f"{config.TEQUILA_BASE}/v2/search"
    headers = {
        "apikey": config.KIWI_API_KEY,
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }
    params = {
        "fly_from": origin_code,
        "fly_to": dest_code,
        "date_from": date_from,
        "date_to": date_to,
        "adults": 1,
        "curr": currency,
        "limit": 1,
        "sort": "price",
        "asc": 1,
    }
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    return data[0] if data else None

def compute_price_per_km(flight: Dict[str, Any]) -> Tuple[float, float, float]:
    """Return (price_per_km, total_price, distance_km)."""
    price = float(flight["price"])
    dist = float(flight["distance"])
    return (price / dist if dist > 0 else float("inf")), price, dist
