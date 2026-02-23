import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

USERS_FILE = "users!.json"
ITEMS_FILE = "items!.json"
TRADES_FILE = "trades!.json"

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def create_test_data_if_empty():
    if not os.path.exists(USERS_FILE):
        test_users = [
            {'username': 'alice', 'password': 'pass123', 'city': 'New York', 'points': 50, 'total_trades': 3},
            {'username': 'bob', 'password': 'pass123', 'city': 'Chicago', 'points': 30, 'total_trades': 2},
            {'username': 'juan', 'password': 'pass123', 'city': 'Manila', 'points': 40, 'total_trades': 4},
             {'username': 'jason', 'password': 'pass123', 'city': 'Cainta', 'points': 35, 'total_trades': 5},
              {'username': 'anne', 'password': 'pass123', 'city': 'Quezon', 'points': 20, 'total_trades': 6},
        ]
        save_data(USERS_FILE, test_users)

    if not os.path.exists(ITEMS_FILE):
        test_items = [
            {'id': 1, 'name': 'Camera', 'desc': 'Film camera', 'condition': 'Good', 'value': 1200.0, 'owner': 'alice'},
            {'id': 2, 'name': 'Guitar', 'desc': 'Acoustic', 'condition': 'Good', 'value': 2500.0, 'owner': 'bob'},
            {'id': 3, 'name': 'Laptop', 'desc': 'Old gaming laptop', 'condition': 'Fair', 'value': 5000.0, 'owner': 'bob'},
            {'id': 4, 'name': 'Phone', 'desc': 'Iphone 13', 'condition': 'Fair', 'value': 13000.0, 'owner': 'alice'},
            {'id': 5, 'name': 'Mini Fan', 'desc': 'JisuLife', 'condition': 'Good', 'value': 800.0, 'owner': 'juan'},
            {'id': 6, 'name': 'Mouse', 'desc': 'Wireless mouse', 'condition': 'Fair', 'value': 600.0, 'owner': 'juan'},
            {'id': 7, 'name': 'GPU', 'desc': 'RTX 5090', 'condition': 'Good', 'value': 150000.0, 'owner': 'jason'},
            {'id': 8, 'name': 'CPU', 'desc': 'Ryzen 9800X3D', 'condition': 'Good', 'value': 30000.0, 'owner': 'jason'},
            {'id': 9, 'name': 'Cat plushie', 'desc': 'Plushie', 'condition': 'Fair', 'value': 100.0, 'owner': 'anne'},
            {'id': 10, 'name': 'Love', 'desc': 'Love is Immeasurable', 'condition': 'Good', 'value': 999999999999999.9, 'owner': 'shinn'},
        ]
        save_data(ITEMS_FILE, test_items)


class BarterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bartering Trade Platform")
        self.root.geometry("700x650")
        
        create_test_data_if_empty()
        self.current_user = None
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="LOGIN", font=("Arial", 20, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Username:").pack()
        self.entry_user = tk.Entry(self.root)
        self.entry_user.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack()
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.process_login, width=20).pack(pady=20)
        tk.Button(self.root, text="Create New Account", command=self.show_register_screen).pack()
        tk.Label(self.root, text="(Try: alice / pass123)", fg="grey").pack(pady=10)

    def process_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        users = load_data(USERS_FILE)
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                self.show_main_menu()
                return
        messagebox.showerror("Error", "Invalid username or password.")

    def show_register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="CREATE ACCOUNT", font=("Arial", 20)).pack(pady=20)
        
        tk.Label(self.root, text="Choose Username:").pack()
        self.reg_user = tk.Entry(self.root)
        self.reg_user.pack()
        
        tk.Label(self.root, text="Choose Password:").pack()
        self.reg_pass = tk.Entry(self.root, show="*")
        self.reg_pass.pack()
        
        tk.Label(self.root, text="Your City:").pack()
        self.reg_city = tk.Entry(self.root)
        self.reg_city.pack()
        
        tk.Button(self.root, text="Register", command=self.process_register).pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen).pack()

    def process_register(self):
        username = self.reg_user.get()
        password = self.reg_pass.get()
        city = self.reg_city.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return

        users = load_data(USERS_FILE)
        for user in users:
            if user['username'] == username:
                messagebox.showerror("Error", "Username already exists!")
                return
        
        new_user = {'username': username, 'password': password, 'city': city, 'points': 0, 'total_trades': 0}
        users.append(new_user)
        save_data(USERS_FILE, users)
        messagebox.showinfo("Success", "Account created! Please login.")
        self.show_login_screen()

    def show_main_menu(self):
        self.clear_screen()
        
        # Header
        welcome_text = f"Welcome, {self.current_user['username']}!"
        tk.Label(self.root, text=welcome_text, font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).pack(anchor="ne", padx=10)

        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_browse = tk.Frame(notebook)
        self.tab_list = tk.Frame(notebook)
        self.tab_my_items = tk.Frame(notebook)
        self.tab_trades = tk.Frame(notebook)
        self.tab_profile = tk.Frame(notebook)
        
        notebook.add(self.tab_browse, text="Browse Items")
        notebook.add(self.tab_list, text="List New Item")
        notebook.add(self.tab_my_items, text="My Items")
        notebook.add(self.tab_trades, text="Trade Offers")
        notebook.add(self.tab_profile, text="My Profile")
        
        self.setup_browse_tab()
        self.setup_list_item_tab()
        self.setup_my_items_tab()
        self.setup_trades_tab()
        self.setup_profile_tab()

    def setup_browse_tab(self):
        # Button bar
        btn_frame = tk.Frame(self.tab_browse)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Refresh Items", command=self.refresh_browse).pack(side=tk.LEFT, padx=5)
        # The 'Make Offer' button
        tk.Button(btn_frame, text="Make Offer for Selected", command=self.start_trade).pack(side=tk.LEFT, padx=5)
        
        # Listbox with Scrollbar
        scrollbar = tk.Scrollbar(self.tab_browse)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.browse_list = tk.Listbox(self.tab_browse, width=80, height=20, yscrollcommand=scrollbar.set)
        self.browse_list.pack(pady=5)
        scrollbar.config(command=self.browse_list.yview)
        
        self.refresh_browse()

    def refresh_browse(self):
        self.browse_list.delete(0, tk.END)
        items = load_data(ITEMS_FILE)
        
        count = 0
        for item in items:
            if item['owner'] != self.current_user['username']:
                # Format: "ItemName | Value: X | Cond: Y | Owner: Z"
                text = f"{item['name']} | Value: ₱{item['value']} | Cond: {item['condition']} | Owner: {item['owner']}"
                self.browse_list.insert(tk.END, text)
                self.browse_list.insert(tk.END, f"   Description: {item['desc']}")
                self.browse_list.insert(tk.END, "-"*50)
                count += 1
        if count == 0:
            self.browse_list.insert(tk.END, "No items available for trade.")

    def start_trade(self):
        selection = self.browse_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to trade for first.")
            return
            
        item_text = self.browse_list.get(selection[0])
        
        if "Description:" in item_text or "---" in item_text:
            messagebox.showwarning("Warning", "Please select the main item line (the one with the Name).")
            return
            
        target_item_name = item_text.split("|")[0].strip()
        
        self.open_trade_popup(target_item_name)

    def open_trade_popup(self, target_item_name):
        popup = tk.Toplevel(self.root)
        popup.title("Make an Offer")
        popup.geometry("350x250")
        
        tk.Label(popup, text=f"You want: {target_item_name}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(popup, text="Select which of YOUR items to give:").pack()
        
        items = load_data(ITEMS_FILE)
        my_items = [i['name'] for i in items if i['owner'] == self.current_user['username']]
        
        if not my_items:
            tk.Label(popup, text="You have no items to trade!", fg="red").pack(pady=10)
            return

        offer_dropdown = ttk.Combobox(popup, values=my_items)
        offer_dropdown.pack(pady=10)
        
        def submit_offer():
            my_offer = offer_dropdown.get()
            if not my_offer:
                messagebox.showwarning("Error", "Please select an item to offer.")
                return
            
            target_owner = ""
            for i in items:
                if i['name'] == target_item_name:
                    target_owner = i['owner']
                    break
            
            trades = load_data(TRADES_FILE) if os.path.exists(TRADES_FILE) else []
            new_trade = {
                "from_user": self.current_user['username'],
                "to_user": target_owner,
                "item_from": my_offer,
                "item_to": target_item_name,
                "status": "pending"
            }
            trades.append(new_trade)
            save_data(TRADES_FILE, trades)
            
            messagebox.showinfo("Success", "Trade offer sent!")
            popup.destroy()

        tk.Button(popup, text="Send Offer", command=submit_offer).pack(pady=20)

    def setup_list_item_tab(self):
        frame = tk.Frame(self.tab_list)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Item Name:").grid(row=0, column=0, pady=5, sticky="e")
        self.list_name = tk.Entry(frame, width=30)
        self.list_name.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Description:").grid(row=1, column=0, pady=5, sticky="e")
        self.list_desc = tk.Entry(frame, width=30)
        self.list_desc.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Condition:").grid(row=2, column=0, pady=5, sticky="e")
        self.list_cond = ttk.Combobox(frame, values=["New", "Like New", "Good", "Fair", "Poor"])
        self.list_cond.set("Good")
        self.list_cond.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Value (₱):").grid(row=3, column=0, pady=5, sticky="e")
        self.list_val = tk.Entry(frame, width=30)
        self.list_val.grid(row=3, column=1, pady=5)
        
        tk.Button(self.tab_list, text="List This Item", command=self.process_list_item).pack(pady=20)

    def process_list_item(self):
        name = self.list_name.get()
        desc = self.list_desc.get()
        try:
            val = float(self.list_val.get())
        except ValueError:
            messagebox.showerror("Error", "Value must be a number")
            return

        items = load_data(ITEMS_FILE)
        new_item = {
            'id': len(items) + 1,
            'name': name, 'desc': desc, 'condition': self.list_cond.get(),
            'value': val, 'owner': self.current_user['username']
        }
        items.append(new_item)
        save_data(ITEMS_FILE, items)
        
        messagebox.showinfo("Success", f"'{name}' listed successfully!")
        self.list_name.delete(0, tk.END)
        self.list_desc.delete(0, tk.END)
        self.list_val.delete(0, tk.END)

    def setup_my_items_tab(self):
        tk.Button(self.tab_my_items, text="Refresh My Items", command=self.refresh_my_items).pack(pady=5)
        self.my_items_list = tk.Listbox(self.tab_my_items, width=80, height=20)
        self.my_items_list.pack(pady=5)
        self.refresh_my_items()

    def refresh_my_items(self):
        self.my_items_list.delete(0, tk.END)
        items = load_data(ITEMS_FILE)
        my_items = [i for i in items if i['owner'] == self.current_user['username']]
        
        if not my_items:
            self.my_items_list.insert(tk.END, "You haven't listed any items yet.")
        else:
            for item in my_items:
                self.my_items_list.insert(tk.END, f"{item['name']} (₱{item['value']}) - {item['condition']}")

    def setup_trades_tab(self):
        btn_frame = tk.Frame(self.tab_trades)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.refresh_trades).pack(side=tk.LEFT, padx=5)
        # Action Buttons
        tk.Button(btn_frame, text="Accept Selected", command=lambda: self.handle_trade_action("accepted")).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reject Selected", command=lambda: self.handle_trade_action("rejected")).pack(side=tk.LEFT, padx=5)
        
        self.trades_list = tk.Listbox(self.tab_trades, width=80, height=20)
        self.trades_list.pack(pady=5)
        self.refresh_trades()

    def refresh_trades(self):
        self.trades_list.delete(0, tk.END)
        trades = load_data(TRADES_FILE)
        if not trades:
            self.trades_list.insert(tk.END, "No trade offers found.")
            return

        sent = [t for t in trades if t['from_user'] == self.current_user['username']]
        received = [t for t in trades if t['to_user'] == self.current_user['username']]

        if received:
            self.trades_list.insert(tk.END, "=== OFFERS RECEIVED ===")
            for t in received:
                self.trades_list.insert(tk.END, f"From: {t['from_user']} | They want: {t['item_to']} | They give: {t['item_from']} | Status: {t['status']}")
                self.trades_list.insert(tk.END, "") # spacer

        if sent:
            self.trades_list.insert(tk.END, "=== OFFERS SENT ===")
            for t in sent:
                self.trades_list.insert(tk.END, f"To: {t['to_user']} | You want: {t['item_to']} | You give: {t['item_from']} | Status: {t['status']}")
                self.trades_list.insert(tk.END, "") # spacer

    def handle_trade_action(self, action):
        selection = self.trades_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a trade offer first")
            return
            
        text = self.trades_list.get(selection[0])
        
        if "From:" not in text:
            messagebox.showwarning("Error", "You can only Accept/Reject offers sent TO you (Offers Received).")
            return

        parts = text.split("|")
        sender = parts[0].replace("From: ", "").strip()
        
        trades = load_data(TRADES_FILE)
        found = False
        
        for trade in trades:
            if trade['from_user'] == sender and trade['to_user'] == self.current_user['username'] and trade['status'] == 'pending':
                trade['status'] = action
                found = True
                if action == "accepted":
                    self.swap_items(trade['item_from'], trade['item_to'], trade['from_user'], trade['to_user'])
                break
        
        if found:
            save_data(TRADES_FILE, trades)
            messagebox.showinfo("Success", f"Trade {action}!")
            self.refresh_trades()
            self.refresh_my_items()
        else:
            messagebox.showerror("Error", "Trade not found or already processed.")

    def swap_items(self, item_from, item_to, user_a, user_b):
        items = load_data(ITEMS_FILE)
        for item in items:
            if item['name'] == item_from:
                item['owner'] = user_b # User B (You) gets the item offered
            elif item['name'] == item_to:
                item['owner'] = user_a # User A (Sender) gets your item
        save_data(ITEMS_FILE, items)

    def setup_profile_tab(self):
        frame = tk.Frame(self.tab_profile)
        frame.pack(pady=30, padx=30, anchor="w")
        
        def add_info(label, value):
            tk.Label(frame, text=label, font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=value, font=("Arial", 12)).pack(anchor="w", pady=(0, 10))

        items = load_data(ITEMS_FILE)
        item_count = len([i for i in items if i['owner'] == self.current_user['username']])

        add_info("Username:", self.current_user['username'])
        add_info("City:", self.current_user['city'])
        add_info("Points:", str(self.current_user['points']))
        add_info("Items Listed:", str(item_count))

if __name__ == "__main__":
    root = tk.Tk()
    app = BarterGUI(root)
root.mainloop()