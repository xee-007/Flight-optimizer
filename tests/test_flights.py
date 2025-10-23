import requests_mock
from helpers import search_cheapest_oneway
from config import config

def test_search_cheapest_oneway_returns_cheapest():
    with requests_mock.Mocker() as m:
        m.get(
            f"{config.TEQUILA_BASE}/v2/search",
            json={
                "data": [
                    {
                        "price": 99,
                        "distance": 1200,
                        "flyFrom": "LON",
                        "flyTo": "PAR"
                    }
                ]
            },
            status_code=200,
        )
        flight = search_cheapest_oneway("LON", "PAR", currency="USD")
        assert flight is not None
        assert flight["price"] == 99
        assert flight["distance"] == 1200

def test_search_cheapest_oneway_no_results():
    with requests_mock.Mocker() as m:
        m.get(
            f"{config.TEQUILA_BASE}/v2/search",
            json={"data": []},
            status_code=200,
        )
        flight = search_cheapest_oneway("LON", "PAR", currency="USD")
        assert flight is None
