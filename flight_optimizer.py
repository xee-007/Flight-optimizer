"""
Find the cheapest flight per kilometer using the Kiwi (Tequila) API.
Usage:
  python flight_optimizer.py --from "London" --to "Paris" "Rome" "Berlin"
"""
import argparse
import sys
from typing import List, Optional, Tuple
from helpers import resolve_city_code, search_cheapest_oneway, compute_price_per_km

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Find the cheapest flight per kilometer.")
    p.add_argument("--from", dest="origin", required=True, help="Departure city (e.g., 'London')")
    p.add_argument("--to", dest="destinations", required=True, nargs="+", help="Destination cities")
    p.add_argument("--currency", default="USD", help="Currency (default: USD)")
    return p.parse_args(argv)

def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        origin_code, origin_name = resolve_city_code(args.origin)
    except Exception as e:
        print(f"[error] Failed to resolve origin '{args.origin}': {e}", file=sys.stderr)
        return 2

    dests: List[Tuple[str, str]] = []
    for d in args.destinations:
        try:
            code, name = resolve_city_code(d)
            dests.append((code, name))
        except Exception as e:
            print(f"[warn] Skipping '{d}': {e}")

    if not dests:
        print("[error] No destination cities could be resolved.")
        return 3

    print(f"Origin: {origin_name} ({origin_code})")
    print("Searching cheapest $/km in the next ~24 hours...\n")

    best = None
    for dest_code, dest_name in dests:
        try:
            flight = search_cheapest_oneway(origin_code, dest_code, args.currency)
            if not flight:
                print(f"[info] No flights found: {origin_code} → {dest_code}")
                continue
            ppkm, price, dist = compute_price_per_km(flight)
            print(f"- {origin_code} → {dest_code}: ${price:.2f} / {dist:.0f}km = ${ppkm:.4f}/km")
            if best is None or ppkm < best[0]:
                best = (ppkm, dest_name, dest_code, price, dist)
        except Exception as e:
            print(f"[warn] Failed {origin_code} → {dest_code}: {e}", file=sys.stderr)

    if not best:
        print("\nNo viable flights found in the next ~24 hours.")
        return 4

    ppkm, dest_name, dest_code, price, dist = best
    print(f"\n✅ Best destination: {dest_name}")
    print(f"💲 Price per km: ${ppkm:.4f}/km")
    print(f"(Cheapest fare: ${price:.2f} for ~{dist:.0f} km; route {origin_code}→{dest_code})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
