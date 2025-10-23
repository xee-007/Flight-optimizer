import importlib
import sys

def test_cli_happy_path(monkeypatch, capsys):
    # Import the real helpers module
    import helpers as real_helpers

    # Stub helpers so we don't hit the network
    def fake_resolve_city_code(name):
      mapping = {"London": ("LON", "London"), "Paris": ("PAR", "Paris")}
      return mapping[name]

    def fake_search_cheapest_oneway(origin, dest, currency="USD"):
      # Make PAR win on $/km
      if dest == "PAR":
          return {"price": 80, "distance": 400}   # $0.20/km (best)
      return {"price": 150, "distance": 500}      # $0.30/km

    def fake_compute_price_per_km(flight):
      price = float(flight["price"])
      dist = float(flight["distance"])
      return price / dist, price, dist

    # Monkeypatch the functions on the already-imported module
    monkeypatch.setattr(real_helpers, "resolve_city_code", fake_resolve_city_code)
    monkeypatch.setattr(real_helpers, "search_cheapest_oneway", fake_search_cheapest_oneway)
    monkeypatch.setattr(real_helpers, "compute_price_per_km", fake_compute_price_per_km)

    # Import CLI after monkeypatching helpers (CLI imports helpers at module import)
    import flight_optimizer as cli
    # If CLI was already imported in this session, reload to ensure patched helpers are used
    importlib.reload(cli)

    # Run main with fake argv
    exit_code = cli.main(["--from", "London", "--to", "Paris"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "Origin: London (LON)" in out
    assert ("Best destination: Paris" in out) or ("✅ Best destination: Paris" in out)
