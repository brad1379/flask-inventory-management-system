import requests
from unittest.mock import patch, Mock

from openfoodfacts import fetch_by_barcode, search_by_name


def test_fetch_by_barcode_found():
    fake_response = Mock()
    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "code": "3017620422003",
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, palm oil"
        }
    }

    with patch("openfoodfacts.requests.get", return_value=fake_response):
        product = fetch_by_barcode("3017620422003")

    assert product["product_name"] == "Nutella"
    assert product["brands"] == "Ferrero"
    assert product["barcode"] == "3017620422003"

def test_fetch_by_barcode_not_found():
    fake_response = Mock()
    fake_response.json.return_value = {"status": 0, "status_verbose": "product not found"}

    with patch("openfoodfacts.requests.get", return_value=fake_response):
        product = fetch_by_barcode("000")

    assert product is None

def test_fetch_by_barcode_connection_error():
    with patch("openfoodfacts.requests.get", side_effect=requests.exceptions.ConnectionError):
        product = fetch_by_barcode("123")

    assert product is None

def test_search_by_name():
    fake_response = Mock()
    fake_response.json.return_value = {
        "products": [
            {"code": "1", "product_name": "Almond Milk", "brands": "Silk"},
            {"code": "2", "product_name": "Oat Milk", "brands": "Oatly"}
        ]
    }

    with patch("openfoodfacts.requests.get", return_value=fake_response):
        results = search_by_name("milk")

    assert len(results) == 2
    assert results[0]["product_name"] == "Almond Milk"

def test_search_by_name_connection_error():
    with patch("openfoodfacts.requests.get", side_effect=requests.exceptions.ConnectionError):
        results = search_by_name("milk")

    assert results == []
