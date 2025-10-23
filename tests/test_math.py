from helpers import compute_price_per_km

def test_compute_price_per_km_normal():
    flight = {"price": 100, "distance": 500}
    ppkm, price, dist = compute_price_per_km(flight)
    assert price == 100.0
    assert dist == 500.0
    assert abs(ppkm - 0.2) < 1e-9  # $0.20/km

def test_compute_price_per_km_zero_distance():
    flight = {"price": 50, "distance": 0}
    ppkm, price, dist = compute_price_per_km(flight)
    assert price == 50.0
    assert dist == 0.0
    assert ppkm == float("inf")
