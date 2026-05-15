# ==============================================================
# Personal Finance Manager - Version 1.0
# Author: Guvvala Venkata Narayana
# 
# Improvements over v0.1:
# 1. CLASSES: Transaction data is now an OBJECT, not a plain dict.
#    This means the data and the methods that work on it are bundled together.
# 2. JSON SAVING: Data is now written to a file on disk.
#    When you close and reopen the program, your transactions survive.
# ===============================================================

import datetime
import json          # json lets us convert Python object <-> text files
import os            # os lets us check if a file exists on the hard drive

# ================================================================
# THE TRANSACTION CLASS
# A class is like a blueprint for creating objects.
# Every time we call Transaction(...), Python creats a new object
# based on this blueprint
# =================================================================
class Transaction:
    """
    Represents a single financial transaction.
    Instead of passing 4 separate variable everywhere, we bundle them
    into one neat object. This is the core benifit of OOP.
    """

    def __init__(self, amount, category, date, description=""):
        """
        __init__ is the constructor - it runs automatically when we create
        a Transaction object. 'self' refers to the specific object being created.
        """
        self.amount = amount    # self.amount means "this object's amount"
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        """
        JSON can only save basic Python types (strings, numbers, lists, dicts).
        It CANNOT directly save a Python object.
        This method converts our Transaction object INTO a plain dictionary
        so that json.dump() can save it to a file.
        """
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        This is a CLASS METHOD - it belongs to the class itself, not to 
        one specific object. We use it to go in the reverse direction:
        take a plain dictionary loaded from JSON adn convert it back
        INTO a Transaction object.

        'cls' here means 'Transaction' - so cls(...) is same as Transaction(...)
        """
        return cls(
            data["amount"],
            data["category"],
            data["date"],
            data.get("description", "") # get() returns "" f key is missing
        )
    
    def __str__(self):
        """
        __str__ is a special method. Python calls it automatically when you do
        print(transaction_object). Without it, you'd see something ugly like
        <__main__.Transaction object at 0x7f...>. With it, you see something readable.
        """
        return f"[{self.data}] {self.category:<15} Rs.{self.amount:>8.2f} | {self.description or 'No description'}"
    

# =================================================================
# THE FINANCEMANAGER CLASS
# This class manages the COLLECTION of Transaction objects.
# It handles loading from file, saving to file, and all user operations.
# =================================================================
class FinanceManager:
    """
    The main controller class. Think of it as the 'manger' of a shop
    who keeps track of all transactions, can save the records, and 
    can answer questions like "how much did I spend this month?"
    """

    def __init__(self, filename="data.json"):
        """
        When we create a FinanceManager object, two things happen:
        1. We set the filename where data will be saved.
        2. We immediately load any existing data from that file. 
        """
        self.filename = filename
        self.transactions = []  # start with empty list
        self._load_data()       # then try to fill it from the file
        # The undersocre in _load_data is Python convention meaning
        # "this is a private helper method, not meant to be called from outside"

    def _load_data(self):
        """
        Load transaction data from the JSON file.
        If the file does not exist yet, we simply start with an empty list.
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                # json.load() reads the file and gives us a Python list of dicts
                raw_data = json.load(file)
                # We convert each dict back into a Transaction object
                self.transactions = [Transaction.from_dict(d) for d in raw_data]
                # This is a LIST COMPREHENSION - a compact way to write a for loop
                # that builds a new list. It means "for each dict d in raw_data,
                # create Transactoin.from(d), and collect all results into a list"
            print(f"Loaded {len(self.transactions)} existing transactions(s).")
        else:
            print("No saved data foud. Starting fresh.")

    def _save_data(self):
        """
        Save all current transactions to the JSON file.
        We call this every time a transaction is added, so data is never lost.
        """
        with open(self.filename, "w") as file:
            # json.dump() writes data to the file.
            # [t.to_dict() for t in self.transactions] converts each Transaction
            # object to a dict first, because JSON cannot store objects directly.
            # indent=4 makes the JSON file human-readable (nicely indented).
            json.dump([t.to_dict() for t in self.transactions], file, indent=4)

    def add_transaction(self):
        """Get input from user and add a new transaction."""
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("ERROR: Amount must be a number.")
            return
        
        category = input("Enter category: ").strip()
        if not category:
            print("ERROR: Category cannot be empty.")
            return 
        
        description = input("Enter description (Enter to skip): ").strip()
        today = datetime.date.today().strftime("%Y-%m-%d")

        # This creates ONE Transaction object and assign it to variable 't'
        t = Transaction(amount, category, today, description)

        self.transactions.append(t)
        self._save_data()
        print(f"\nAdded and Saved: {t}")

    def view_all_transactions(self):
        """Display every transaction."""
        if not self.transactions:
            print("No transactions yet.")
            return
        print("\n" + "=" * 60)
        print("            ALL TRANSACTIONS")
        print("=" * 60)
        total = 0
        for i, t in enumerate(self.transactions, start=1):
            print(f" {i:>3}. {t}")
            total += t.amount
        print("-" * 60)
        print(f"  TOTAL: Rs.{total:.2f}")
        print("=" * 60)

    def monthly_summary(self):
        """
        Group transactions by month and show the total for each month.
        We extract the year-month part (first 7 cgaracters) of each date string.
        For example: "2026-05-10" --> "2026-05"
        """
        if not self.transactions:
            print("No data to summarize.")
            return
        
        summary = {} # This will be: {"2026-05": 1500.0, "2026-04": 800.0, ...}
        for t in self.transactions:
            month_key = t.date[:7] # slice first 7 characters: "YYYY-MM"
            # dict.get(key, default) returns the value for key, or default if missing key
            summary[month_key] = summary.get(month_key, 0) + t.amount
                
        print("\n" + "=" * 40) 
        print("     MONTHLY SUMMARY")
        print("=" * 40)
        for month, total in sorted(summary.items()):
            # sorted() on a dict.items() sorts by by key alphabetically,
            # which for "YYYY-MM" format means chronological order
            print(f"  {month}: Rs.{total:.2f}")
        print("=" * 40)

# ==================================================================
# MENU AND MAIN LOOP (same structure as v0.1, but calling class methods)
# ====================================================================

def show_menu():
    print("\n" + "=" * 40)
    print("    PERSONAL FINANCE MANAGER v1.0")
    print("=" * 40)
    print(" 1. Add Transaction")
    print(" 2. View all Transactions")
    print(" 3. Monthly Summary")
    print(" 4. Exit")
    print("=" * 40)

def main():
    # Creating a FinanceManager object. This triggers __init__,
    # which triggers _load_data(), which loads existing transactoins.
    manager = FinanceManager()

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            manager.add_transaction()
        elif choice == "2":
            manager.view_all_transactions()
        elif choice == "3":
            manager.monthly_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()