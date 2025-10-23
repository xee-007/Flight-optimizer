# server.py
from typing import List, Tuple, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, constr

from helpers import resolve_city_code, search_cheapest_oneway, compute_price_per_km

app = FastAPI(title="Flight Optimizer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# ---------- Schemas ----------
class OptimizeRequest(BaseModel):
    origin: constr(strip_whitespace=True, min_length=1)
    destinations: List[constr(strip_whitespace=True, min_length=1)] = Field(min_items=1)
    currency: str = "USD"

class DestinationResult(BaseModel):
    destination: str
    code: str
    price: float
    distance_km: float
    price_per_km: float

class OptimizeResponse(BaseModel):
    best_destination: str
    price_per_km: float
    details: List[DestinationResult]

# ---------- Endpoint ----------
@app.post("/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest):
    # Resolve origin city to metropolitan code (e.g., "London" -> "LON")
    try:
        origin_code, _origin_name = resolve_city_code(req.origin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Origin resolution failed: {e}")

    # Resolve destination cities
    resolved: List[Tuple[str, str]] = []
    for d in req.destinations:
        try:
            code, name = resolve_city_code(d)
            resolved.append((code, name))
        except Exception:
            # skip unresolvable destinations
            pass

    if not resolved:
        raise HTTPException(status_code=400, detail="No destinations resolved.")

    # Search cheapest flight per destination and compute $/km
    results: List[DestinationResult] = []
    for code, name in resolved:
        flight = search_cheapest_oneway(origin_code, code, req.currency)
        if not flight:
            continue
        ppkm, price, dist = compute_price_per_km(flight)
        results.append(DestinationResult(
            destination=name, code=code, price=price, distance_km=dist, price_per_km=ppkm
        ))

    if not results:
        raise HTTPException(status_code=404, detail="No viable flights found in the next ~24 hours.")

    best = min(results, key=lambda r: r.price_per_km)
    return OptimizeResponse(
        best_destination=best.destination,
        price_per_km=best.price_per_km,
        details=results,
    )
