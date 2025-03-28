import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        
        # Create database connection
        self.conn = sqlite3.connect('inventory.db')
        self.c = self.conn.cursor()
        
        # Create table if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS inventory
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         quantity INTEGER NOT NULL,
                         price REAL NOT NULL,
                         category TEXT,
                         description TEXT)''')
        self.conn.commit()
        
        # Create UI
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Frame for form
        form_frame = ttk.LabelFrame(self.root, text="Inventory Item")
        form_frame.pack(pady=10, padx=10, fill="x")
        
        # Entry fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(form_frame)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(form_frame)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update Item", command=self.update_item).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_fields).grid(row=0, column=3, padx=5)
        
        # Treeview for displaying inventory
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Quantity", "Price", "Category"), show="headings")
        self.tree.pack(fill="both", expand=True)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Category", text="Category")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Quantity", width=80)
        self.tree.column("Price", width=80)
        self.tree.column("Category", width=100)
        
        # Bind treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    def load_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch data from database
        self.c.execute("SELECT id, name, quantity, price, category FROM inventory")
        rows = self.c.fetchall()
        
        # Insert data into treeview
        for row in rows:
            self.tree.insert("", "end", values=row)
    
    def add_item(self):
        try:
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            category = self.category_entry.get()
            description = self.desc_entry.get()
            
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
                
            self.c.execute("INSERT INTO inventory (name, quantity, price, category, description) VALUES (?, ?, ?, ?, ?)",
                          (name, quantity, price, category, description))
            self.conn.commit()
            
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Item added successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price")
            
    def update_item(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update")
            return
            
        try:
            id = self.tree.item(selected)['values'][0]
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
            category = self.category_entry.get()
            description = self.desc_entry.get()
            
            self.c.execute("UPDATE inventory SET name=?, quantity=?, price=?, category=?, description=? WHERE id=?",
                          (name, quantity, price, category, description, id))
            self.conn.commit()
            
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Item updated successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price")
            
    def delete_item(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            id = self.tree.item(selected)['values'][0]
            self.c.execute("DELETE FROM inventory WHERE id=?", (id,))
            self.conn.commit()
            self.load_data()
            self.clear_fields()
            
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        
    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            item = self.tree.item(selected)
            values = item['values']
            self.clear_fields()
            
            self.name_entry.insert(0, values[1])
            self.quantity_entry.insert(0, values[2])
            self.price_entry.insert(0, values[3])
            self.category_entry.insert(0, values[4])
            
            # Get description from database
            self.c.execute("SELECT description FROM inventory WHERE id=?", (values[0],))
            desc = self.c.fetchone()[0]
            self.desc_entry.insert(0, desc if desc else "")
The task is to create an Inventory Management desktop application. However, there are currently no visible files in the working directory, which means I need to start from scratch. I will need to create the necessary files and structure for the application. 

Since there are no existing files, I will proceed to create a basic structure for the inventory management app, which typically includes:
1. A main application file (e.g., `app.py`).
2. A user interface file (e.g., `ui.py`).
3. A requirements file (e.g., `requirements.txt`) to manage dependencies.

I will create these files and then outline the plan for the application.
</thinking>

<create_file>
<path>app.py</path>
<content>
import tkinter as tk
from tkinter import messagebox

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Welcome to Inventory Management")
        self.label.pack(pady=20)

        self.add_item_button = tk.Button(root, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=10)

        self.view_items_button = tk.Button(root, text="View Items", command=self.view_items)
        self.view_items_button.pack(pady=10)

    def add_item(self):
        messagebox.showinfo("Add Item", "Functionality to add item will be implemented.")

    def view_items(self):
        messagebox.showinfo("View Items", "Functionality to view items will be implemented.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()