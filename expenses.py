import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import datetime

# Initialize main application window
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Initialize variables
        self.entries = []
        self.total_debited = 0
        self.total_credited = 0

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Type dropdown
        tk.Label(self.root, text="Type:").grid(row=0, column=0, padx=10, pady=10)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.root, textvariable=self.type_var, values=["debit", "credit"], state="readonly")
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.type_dropdown.set("debit")

        # Amount entry
        tk.Label(self.root, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Category entry
        tk.Label(self.root, text="Category:").grid(row=2, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10)

        # Date entry
        tk.Label(self.root, text="Date:").grid(row=3, column=0, padx=10, pady=10)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=3, column=1, padx=10, pady=10)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        # Add Entry Button
        self.add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Entries Table
        self.tree = ttk.Treeview(self.root, columns=("Type", "Amount", "Category", "Date"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Totals
        self.total_debited_label = tk.Label(self.root, text=f"Total Debited: $0.00")
        self.total_debited_label.grid(row=6, column=0, padx=10, pady=10)
        self.total_credited_label = tk.Label(self.root, text=f"Total Credited: $0.00")
        self.total_credited_label.grid(row=6, column=1, padx=10, pady=10)

        # Export CSV Button
        self.export_button = tk.Button(self.root, text="Export as CSV", command=self.export_csv)
        self.export_button.grid(row=7, column=0, columnspan=2, pady=10)

    def add_entry(self):
        type = self.type_var.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount or not category or not date:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        if type == "debit":
            self.total_debited += amount
        else:
            self.total_credited += amount

        self.entries.append({"Type": type, "Amount": amount, "Category": category, "Date": date})
        self.update_table()
        self.update_totals()
        self.clear_entries()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in self.entries:
            self.tree.insert("", "end", values=(entry["Type"], f"${entry['Amount']:.2f}", entry["Category"], entry["Date"]))

    def update_totals(self):
        self.total_debited_label.config(text=f"Total Debited: ${self.total_debited:.2f}")
        self.total_credited_label.config(text=f"Total Credited: ${self.total_credited:.2f}")

    def clear_entries(self):
        self.amount_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

    def export_csv(self):
        df = pd.DataFrame(self.entries)
        df.to_csv('expenses.csv', index=False)
        messagebox.showinfo("Export Success", "Data exported to expenses.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
