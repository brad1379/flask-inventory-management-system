from flask import Flask, request, jsonify
from openfoodfacts import fetch_by_barcode, search_by_name

app = Flask(__name__)

class Product:
    def __init__(self, id, name, price=0.0, stock=0, barcode=None, brands=None, ingredients_text=None):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.barcode = barcode
        self.brands = brands
        self.ingredients_text = ingredients_text

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "barcode": self.barcode,
            "brands": self.brands,
            "ingredients_text": self.ingredients_text
        }

# Mock database - made to look like OpenFoodFacts data
products = [
    Product(1, "Banana", 0.25, 100),
    Product(2, "Organic Almond Milk", 3.99, 24, None, "Silk", "Filtered water, almonds, cane sugar, sea salt"),
    Product(3, "Nutella", 5.49, 12, "3017620422003", "Nutella, Ferrero", "Sugar, palm oil, hazelnuts, skimmed milk powder, cocoa")
]

def find_product(id):
    return next((prod for prod in products if prod.id == id), None)

# Checks price and stock if they were sent. Returns an error message or None
def check_price_and_stock(data):
    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return "Price must be a number that is 0 or more"
    if "stock" in data:
        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return "Stock must be a whole number that is 0 or more"
    return None

# Fetch all items
@app.route("/inventory", methods=["GET"])
def get_products():
    return jsonify([prod.to_dict() for prod in products]), 200


# Fetch single item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = find_product(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict()), 200

# Add a new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    error = check_price_and_stock(data)
    if error:
        return jsonify({"error": error}), 400

    name = data.get("name")
    brands = data.get("brands")
    ingredients_text = data.get("ingredients_text")
    barcode = data.get("barcode")

    # If there's a barcode, get extra details from OpenFoodFacts
    if barcode:
        details = fetch_by_barcode(barcode)
        if details:
            if not name:
                name = details["product_name"]
            if not brands:
                brands = details["brands"]
            if not ingredients_text:
                ingredients_text = details["ingredients_text"]

    if not name:
        return jsonify({"error": "Item needs a name (or a barcode that is on OpenFoodFacts)"}), 400

    if products:
        new_id = products[-1].id + 1
    else:
        new_id = 1

    item = Product(new_id, name, data.get("price", 0.0), data.get("stock", 0), barcode, brands, ingredients_text)
    products.append(item)
    return jsonify(item.to_dict()), 201

# Update an item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = find_product(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    error = check_price_and_stock(data)
    if error:
        return jsonify({"error": error}), 400

    if "name" in data:
        item.name = data["name"]
    if "price" in data:
        item.price = data["price"]
    if "stock" in data:
        item.stock = data["stock"]
    if "brands" in data:
        item.brands = data["brands"]
    if "ingredients_text" in data:
        item.ingredients_text = data["ingredients_text"]

    return jsonify(item.to_dict()), 200

# Remove an item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def remove_item(id):
    item = find_product(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    products.remove(item)
    return jsonify({"message": f"Item {id} deleted"}), 200

# Look up a product on OpenFoodFacts using ?barcode= or ?name=
@app.route("/lookup", methods=["GET"])
def lookup_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if barcode:
        product = fetch_by_barcode(barcode)
        if not product:
            return jsonify({"error": "Product not found on OpenFoodFacts"}), 404
        return jsonify(product), 200

    if name:
        return jsonify(search_by_name(name)), 200

    return jsonify({"error": "Please search with a barcode or name"}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
