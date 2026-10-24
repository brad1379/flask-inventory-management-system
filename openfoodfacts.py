import requests

BASE_URL = "https://world.openfoodfacts.org"
# OpenFoodFacts blocks requests that don't say what app is calling it
HEADERS = {"User-Agent": "FlaskInventoryManagementSystem/1.0"}


# Look up a product by barcode. Returns a dict with the product info, or None if it wasn't found
def fetch_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError):
        print("Error: could not get data from OpenFoodFacts")
        return None

    if data.get("status") != 1:
        return None

    product = data["product"]
    return {
        "barcode": product.get("code"),
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
    }


# Search for products by name. Returns a list of products (empty if nothing was found)
def search_by_name(name):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError):
        print("Error: could not get data from OpenFoodFacts")
        return []

    results = []
    for product in data.get("products", []):
        results.append({
            "barcode": product.get("code"),
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "ingredients_text": product.get("ingredients_text"),
        })
    return results
