# Summative Lab: Python REST API with Flask- Inventory Management System 

### Task 1: Define the Problem 
Analyze and plan each necessary route.
Build a user interface to interact with each route.
Build Flask endpoints to trigger upon user action.
Connect to the OpenFoodFacts api to get specific data from the database.
Update simulated data storage by updating an array.

### Task 2: Determine the Design 
For each planned route, determine the necessary route inputs as well as the output of each route. 
<br>
- Determine what it will change regarding the data given.
- Determine when each route will be triggered within the CLI application.
- Utilizingthe  OpenFoodFacts database, build a mock database in an array.

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