import pytest
from unittest.mock import patch

import app as app_module
from app import app, Product


@pytest.fixture
def client():
    # Reset the products list before each test so tests don't affect each other
    app_module.products.clear()
    app_module.products.append(Product(1, "Banana", 0.25, 100))
    app_module.products.append(Product(2, "Apple", 0.50, 50))
    return app.test_client()


def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Banana"

def test_get_item_not_found(client):
    response = client.get("/inventory/99")
    assert response.status_code == 404

def test_add_item(client):
    response = client.post("/inventory", json={"name": "Milk", "price": 2.99, "stock": 10})
    assert response.status_code == 201
    assert response.get_json()["id"] == 3
    assert response.get_json()["name"] == "Milk"

def test_add_item_without_name(client):
    response = client.post("/inventory", json={"price": 2.99})
    assert response.status_code == 400

def test_add_item_with_negative_price(client):
    response = client.post("/inventory", json={"name": "Milk", "price": -1})
    assert response.status_code == 400

def test_add_item_with_barcode_uses_openfoodfacts(client):
    fake_product = {
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil"
    }
    with patch("app.fetch_by_barcode", return_value=fake_product):
        response = client.post("/inventory", json={"barcode": "3017620422003", "price": 5.49, "stock": 3})

    assert response.status_code == 201
    assert response.get_json()["name"] == "Nutella"
    assert response.get_json()["brands"] == "Ferrero"

def test_update_item(client):
    response = client.patch("/inventory/1", json={"stock": 75})
    assert response.status_code == 200
    assert response.get_json()["stock"] == 75

def test_update_item_not_found(client):
    response = client.patch("/inventory/99", json={"stock": 75})
    assert response.status_code == 404

def test_update_item_with_bad_stock(client):
    response = client.patch("/inventory/1", json={"stock": "lots"})
    assert response.status_code == 400

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert client.get("/inventory/1").status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/inventory/99")
    assert response.status_code == 404

def test_lookup_by_barcode(client):
    fake_product = {"barcode": "123", "product_name": "Nutella", "brands": "Ferrero", "ingredients_text": None}
    with patch("app.fetch_by_barcode", return_value=fake_product):
        response = client.get("/lookup?barcode=123")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Nutella"

def test_lookup_barcode_not_found(client):
    with patch("app.fetch_by_barcode", return_value=None):
        response = client.get("/lookup?barcode=000")
    assert response.status_code == 404

def test_lookup_by_name(client):
    with patch("app.search_by_name", return_value=[{"product_name": "Almond Milk"}]):
        response = client.get("/lookup?name=almond milk")
    assert response.status_code == 200
    assert response.get_json()[0]["product_name"] == "Almond Milk"

def test_lookup_with_no_search(client):
    response = client.get("/lookup")
    assert response.status_code == 400
