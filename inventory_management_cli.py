import sqlite3

class InventoryCLI:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS inventory
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         quantity INTEGER NOT NULL,
                         price REAL NOT NULL,
                         category TEXT,
                         description TEXT)''')
        self.conn.commit()

    def add_item(self, name, quantity, price, category, description):
        self.c.execute("INSERT INTO inventory (name, quantity, price, category, description) VALUES (?, ?, ?, ?, ?)",
                       (name, quantity, price, category, description))
        self.conn.commit()
        print("Item added successfully.")

    def view_items(self):
        self.c.execute("SELECT * FROM inventory")
        rows = self.c.fetchall()
        for row in rows:
            print(row)

    def update_item(self, item_id, name, quantity, price, category, description):
        self.c.execute("UPDATE inventory SET name=?, quantity=?, price=?, category=?, description=? WHERE id=?",
                       (name, quantity, price, category, description, item_id))
        self.conn.commit()
        print("Item updated successfully.")

    def delete_item(self, item_id):
        self.c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()
        print("Item deleted successfully.")

    def close(self):
        self.conn.close()

def main():
    cli = InventoryCLI()
    while True:
        print("\nInventory Management CLI")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            cli.add_item(name, quantity, price, category, description)
        elif choice == '2':
            cli.view_items()
        elif choice == '3':
            item_id = int(input("Enter item ID to update: "))
            name = input("Enter new item name: ")
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            category = input("Enter new category: ")
            description = input("Enter new description: ")
            cli.update_item(item_id, name, quantity, price, category, description)
        elif choice == '4':
            item_id = int(input("Enter item ID to delete: "))
            cli.delete_item(item_id)
        elif choice == '5':
            cli.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()