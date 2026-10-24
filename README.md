# Summative Lab: Python REST API with Flask- Inventory Management System 

A Flask REST API for managing a store's food inventory, with a command line interface (CLI) for employees and product lookups from the [OpenFoodFacts API](https://world.openfoodfacts.org/).

## Project Files

| File | What it does |
| --- | --- |
| `app.py` | Flask API with the CRUD routes and the mock inventory data |
| `openfoodfacts.py` | Functions that look up products on OpenFoodFacts by barcode or name |
| `cli.py` | Menu-based command line app that talks to the Flask API |
| `tests/` | Pytest tests for the API, CLI, and OpenFoodFacts functions |

## Installation and Setup

1. Clone the repo and `cd` into it
2. Install the dependencies:
   ```bash
   pipenv install
   ```
3. Start the API (runs on http://localhost:5555):
   ```bash
   pipenv run python app.py
   ```
4. In a second terminal, start the CLI:
   ```bash
   pipenv run python cli.py
   ```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/inventory` | Get all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Add an item. Needs a `name`, or a `barcode` that is on OpenFoodFacts |
| PATCH | `/inventory/<id>` | Update an item's `name`, `price`, `stock`, `brands`, or `ingredients_text` |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/lookup?barcode=<barcode>` | Look up a product on OpenFoodFacts by barcode |
| GET | `/lookup?name=<name>` | Search OpenFoodFacts by product name (up to 5 results) |

Each item looks like this:

```json
{
  "id": 3,
  "name": "Nutella",
  "price": 5.49,
  "stock": 12,
  "barcode": "3017620422003",
  "brands": "Nutella, Ferrero",
  "ingredients_text": "Sugar, palm oil, hazelnuts, skimmed milk powder, cocoa"
}
```

If you add an item with a barcode, the API fills in the name, brand, and ingredients from OpenFoodFacts (anything you type yourself is kept). For example:

```bash
curl -X POST http://localhost:5555/inventory -H "Content-Type: application/json" -d '{"barcode": "3017620422003", "price": 5.49, "stock": 12}'
```

Errors come back as JSON with a status code, like `{"error": "Item not found"}` with a 404.

## Using the CLI

```
Welcome to the Food Inventory Management System!

What would you like to do?
 1. View all products
 2. View one item
 3. Add an item
 4. Update price/stock
 5. Delete an item
 6. Find an item on OpenFoodFacts
 7. Exit
```

Example of adding an item by barcode:

```
3
Barcode (press Enter to skip): 3017620422003
Name (press Enter to use the name from OpenFoodFacts):
Price: 5.49
Stock: 12
Item added!
[4] Nutella - $5.49 (12 in stock)
    Brand: Nutella, Ferrero
    Barcode: 3017620422003
    Ingredients: sugar, palm oil
```

The CLI asks again if you type something invalid (like letters for a price), and shows a message if the API isn't running.

## Running the Tests

```bash
pipenv run pytest
```

The tests use `unittest.mock` so they don't call the real OpenFoodFacts API or need the server running.

---

# Lab Instructions

## Scenario

You have been hired by a small retail company to develop an inventory management system. This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (e.g., OpenFoodFacts API) to supplement product details.

You are tasked with creating an administrator portal for an e-commerce website, which will include.

- A Flask-based REST API with CRUD operations for managing inventory.
- An external API integration to fetch product details by barcode or name.
- A CLI-based interface to interact with the API.
- Unit tests to validate functionality and interactions.


## Instructions 
### Task 1: Define the Problem 
Analyze and plan each necessary route.
Build a user interface to interact with each route.
Build Flask endpoints to trigger upon user action.
Connect to the OpenFoodFacts api to get specific data from the database.
Update simulated data storage by updating an array.

### Task 2: Determine the Design 
For each planned route, determine the necessary route inputs as well as the output of each route. 

- Determine what it will change regarding the data given.
- Determine when each route will be triggered within the CLI application.
- Utilizing the OpenFoodFacts database, build a mock database in an array.

 The data should resemble what the OpenFoodFacts API may contain: 

```JSON
{
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, ..."
    // Additional product information
  }
}
```
It is up to you to determine what data you may want to store. Ensure each item in your database array contains an ID.

### Task 3: Develop Code

#### Task 1: File Setup
* Initialize or clone a new Python project.
    * Install necessary python installs like Flask.
    * Use GitHub.

#### Task 2: API Design
Define API endpoints following RESTful conventions:
```http
    GET /inventory → Fetch all items
    GET /inventory/<id> → Fetch a single item
    POST /inventory → Add a new item
    PATCH /inventory/<id> → Update an item
    DELETE /inventory/<id> → Remove an item
```
Implement Flask routing and request handling.
Update the temporary array to simulate storage.
#### Task 3: Fetch Data
- Use the OpenFoodFacts API to fetch product details.
- Implement a function that queries the external API using a barcode or product name.
- Enhance stored inventory data with additional details from the API.

#### Task 4: CLI Frontend
- Develop a CLI tool to interact with the API.
- Allow users to:

    - Add new inventory items.
    - View inventory details.
    - Update item prices or stock levels.
    - Delete products.
    - Find item on api.

- Ensure error handling for invalid inputs and API failures.

### Task 4: Test and Debug

1. Write unit tests for:

    - API endpoints (GET, POST, PATCH, DELETE)
    - CLI commands
    - External API interactions

2. Use pytest and unittest.mock to simulate API responses.
3. Debug with Flask Debug Mode and Postman for API validation.

### Task 5: Document and Maintain

- Write a README.md with:

    - Installation and setup instructions
    - API endpoint details
    - Example usage of CLI commands
    - Ensure clear code comments and maintainability.

- Push the project to GitHub with a structured repository.