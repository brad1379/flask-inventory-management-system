import requests

BASE_URL = "http://localhost:5555"

MENU = "\nWhat would you like to do?\n 1. View all products\n 2. View one item\n 3. Add an item\n 4. Update price/stock\n 5. Delete an item\n 6. Find an item on OpenFoodFacts\n 7. Exit\n"


# Keeps asking until the user types a whole number
def get_int(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number < 0:
                print("Number can't be negative")
            else:
                return number
        except ValueError:
            print("Please enter a whole number")

# Keeps asking until the user types a number (decimals allowed)
def get_float(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number < 0:
                print("Number can't be negative")
            else:
                return number
        except ValueError:
            print("Please enter a number")

def print_item(item):
    print(f"[{item['id']}] {item['name']} - ${item['price']:.2f} ({item['stock']} in stock)")
    if item.get("brands"):
        print(f"    Brand: {item['brands']}")
    if item.get("barcode"):
        print(f"    Barcode: {item['barcode']}")
    if item.get("ingredients_text"):
        print(f"    Ingredients: {item['ingredients_text']}")

def view_all():
    response = requests.get(f"{BASE_URL}/inventory")
    items = response.json()
    if len(items) == 0:
        print("There are no items in the inventory")
    for item in items:
        print_item(item)

def view_one():
    id = get_int("Enter the item ID: ")
    response = requests.get(f"{BASE_URL}/inventory/{id}")
    if response.status_code == 200:
        print_item(response.json())
    else:
        print(response.json()["error"])

def add_item():
    new_item = {}

    barcode = input("Barcode (press Enter to skip): ").strip()
    if barcode:
        new_item["barcode"] = barcode
        name = input("Name (press Enter to use the name from OpenFoodFacts): ").strip()
    else:
        name = input("Name: ").strip()
        while name == "":
            print("Name can't be empty")
            name = input("Name: ").strip()

    if name:
        new_item["name"] = name
    new_item["price"] = get_float("Price: ")
    new_item["stock"] = get_int("Stock: ")

    response = requests.post(f"{BASE_URL}/inventory", json=new_item)
    if response.status_code == 201:
        print("Item added!")
        print_item(response.json())
    else:
        print(response.json()["error"])

def update_item():
    id = get_int("Enter the item ID: ")
    choice = input("What do you want to update?\n 1. Price\n 2. Stock\n")

    if choice == "1":
        updates = {"price": get_float("New price: ")}
    elif choice == "2":
        updates = {"stock": get_int("New stock: ")}
    else:
        print("Invalid choice")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{id}", json=updates)
    if response.status_code == 200:
        print("Item updated!")
        print_item(response.json())
    else:
        print(response.json()["error"])

def delete_item():
    id = get_int("Enter the item ID: ")
    confirm = input(f"Are you sure you want to delete item {id}? (y/n) ")
    if confirm.lower() != "y":
        print("Item was not deleted")
        return

    response = requests.delete(f"{BASE_URL}/inventory/{id}")
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(response.json()["error"])

def find_on_api():
    choice = input("Search by:\n 1. Barcode\n 2. Name\n")

    if choice == "1":
        barcode = input("Barcode: ")
        response = requests.get(f"{BASE_URL}/lookup", params={"barcode": barcode})
        if response.status_code == 200:
            products = [response.json()]
        else:
            print(response.json()["error"])
            return
    elif choice == "2":
        name = input("Product name: ")
        response = requests.get(f"{BASE_URL}/lookup", params={"name": name})
        products = response.json()
    else:
        print("Invalid choice")
        return

    if len(products) == 0:
        print("No products found")
    for product in products:
        print(f"- {product['product_name']} (barcode: {product['barcode']})")
        if product.get("brands"):
            print(f"    Brand: {product['brands']}")
        if product.get("ingredients_text"):
            print(f"    Ingredients: {product['ingredients_text']}")

def main():
    print("Welcome to the Food Inventory Management System!")

    while True:
        choice = input(MENU)

        try:
            if choice == "1":
                view_all()
            elif choice == "2":
                view_one()
            elif choice == "3":
                add_item()
            elif choice == "4":
                update_item()
            elif choice == "5":
                delete_item()
            elif choice == "6":
                find_on_api()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter a number 1-7")
        except requests.exceptions.ConnectionError:
            print("Could not connect to the server. Make sure app.py is running.")


if __name__ == "__main__":
    main()
