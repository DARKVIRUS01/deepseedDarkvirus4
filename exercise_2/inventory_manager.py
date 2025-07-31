"""
SMART INVENTORY MANAGER.
"""
import os
import ast

DATA_FILE = os.path.join(os.path.dirname(__file__), "inventory_data.py")

# Load inventory from file
def load_inventory():
    inventory = {}
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ',' in line:
                    item, data_str = line.split(',', 1)
                    try:
                        data = ast.literal_eval(data_str)
                        if isinstance(data, dict):
                            inventory[item] = data
                    except Exception:
                        pass
    except Exception:
        pass
    return inventory

# Save inventory to file
def save_inventory(inventory):
    with open(DATA_FILE, "w") as f:
        f.write("# Inventory data: each line is 'item_name,{data}'\n")
        for item, data in inventory.items():
            f.write(f"{item},{data}\n")

def format_currency(value):
    return f"{value:,.2f}cfa"

def add_item(inventory):
    name = input("Enter item name: ").strip()
    if name in inventory:
        print("Item already exists.")
        return
    try:
        price = float(input("Enter price: "))
        stock = int(input("Enter stock quantity: "))
        category = input("Enter category: ").strip()
        inventory[name] = {"price": price, "stock": stock, "category": category}
        save_inventory(inventory)
        print(f"Added item '{name}'.")
    except ValueError:
        print("Invalid input. Price must be a number, stock must be an integer.")

def update_stock(inventory):
    name = input("Enter item name: ").strip()
    if name not in inventory:
        print(f"Item '{name}' not found.")
        return
    try:
        change = int(input("Enter stock change (+/-): "))
        inventory[name]["stock"] += change
        if inventory[name]["stock"] < 0:
            inventory[name]["stock"] = 0
        save_inventory(inventory)
        print(f"Updated stock for '{name}'. New stock: {inventory[name]['stock']}")
    except ValueError:
        print("Invalid input. Stock change must be an integer.")

def search_by_category(inventory):
    category = input("Category to search: ").strip()
    found = [ (item, data) for item, data in inventory.items() if data["category"].lower() == category.lower() ]
    if found:
        print(f"Found {len(found)} items in {category}:")
        for item, data in found:
            print(f"• {item} - {format_currency(data['price'])} ({data['stock']} in stock)")
    else:
        print(f"No items found in category '{category}'.")

def low_stock_alert(inventory):
    low_items = [ (item, data["stock"]) for item, data in inventory.items() if data["stock"] <= 5 ]
    if low_items:
        print("\n⚠️ LOW STOCK ALERT:")
        for item, stock in low_items:
            print(f"- {item} ({stock} units remaining)")
    else:
        print("No low stock items.")

def inventory_value(inventory):
    total = sum(data["price"] * data["stock"] for data in inventory.values())
    print(f"Current Inventory Value: {format_currency(total)}")

def main():
    inventory = load_inventory()
    while True:
        print("\n=== SMART INVENTORY MANAGER ===")
        inventory_value(inventory)
        low_stock_alert(inventory)
        print("\n1. Add New Item")
        print("2. Update Stock")
        print("3. Search Items by Category")
        print("4. Check Low Stock Items")
        print("5. Calculate Total Inventory Value")
        print("6. Exit")
        choice = input("Choose option: ").strip()
        if choice == '1':
            add_item(inventory)
        elif choice == '2':
            update_stock(inventory)
        elif choice == '3':
            search_by_category(inventory)
        elif choice == '4':
            low_stock_alert(inventory)
        elif choice == '5':
            inventory_value(inventory)
        elif choice == '6':
            print("Exiting Inventory Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
