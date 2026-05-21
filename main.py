import json
from datetime import date, datetime
from colorama import init, Fore, Style
init(autoreset=True)
import os
import csv
#print(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter Text Heres".ljust(120) + Fore.CYAN + "║")
class Transaction:
    def __init__(self, amount, category, date, description=""):
        self.amount = float(amount)  # ensure it's a float
        self.category = category
        self.date = date
        self.description = description

    def __str__(self):
        if self.description:
            return f"[{self.date}] {self.category}: ₹{self.amount} ({self.description})"
        else:
            return f"[{self.date}] {self.category}: ₹{self.amount}"
        
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        if not all(key in data for key in ["amount", "category", "date"]):
            raise ValueError(Fore.CYAN + "║" + Fore.WHITE+ f"  Missing required fields in transaction data: {data}".ljust(120) + Fore.CYAN + "║")
        return cls(
            amount = data["amount"],
            category = data["category"],
            date = data["date"],
            description = data.get("description", "")
        )
        
class FinanceManager:
    def __init__(self, filename="finance_data.json"):
        self.transactions = []
        # Get the directory where this script (main.py) is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(script_dir, filename)

        # Budget storage
        self.budget_file = os.path.join(script_dir, "budgets.json")
        self.budgets = {} # category -> limit
        self._load_budgets() # load existing budgets, if any

    def _load_budgets(self):
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, "r") as f:
                    self.budgets = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.budgets = {}
        else:
            self.budgets = {}

    def _save_budgets(self):
        with open(self.budget_file, "w") as f:
            json.dump(self.budgets, f, indent=4)

    def set_budget(self):
        category = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter category to set budget for: ".ljust(120) + Fore.CYAN + "║").strip()
        if not category:
             print(Fore.CYAN + "║" + Fore.RED + "  ❌ Category cannot be empty.".ljust(118) + Fore.CYAN + " ║")
             return
        while True:
            raw = input(Fore.CYAN + "║" + Fore.WHITE + f"  Enter monthly budget for '{category}': Rs. ".ljust(120) + Fore.CYAN + "║").strip()
            try:
                limit = float(raw)
                if limit < 0:
                    print(Fore.CYAN + "║" + Fore.RED + "  ❌ Budget must be a positive number.".ljust(118) + Fore.CYAN + " ║")
                    continue
                break
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid number. Please enter digits only.".ljust(118) + Fore.CYAN + " ║")

        self.budgets[category] = limit
        self._save_budgets() 
        print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Budget set: Rs.{limit:.2f}/month for '{category}'".ljust(120) + Fore.CYAN + " ║")

    def check_budget_status(self):
        if not self.budgets:
            print(Fore.CYAN + "║" + Fore.YELLOW + "  No budgets set yet. Use 'Set Budget' first.".ljust(120) + Fore.CYAN + "║")
            return

        current_month = date.today().strftime("%Y-%m")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.YELLOW + f"  BUDGET STATUS - {current_month}".center(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")   
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        for category, limit in self.budgets.items():
            # Filter transactions: must match category (case-insensitive) AND be in current month
            spent = abs(sum(t.amount for t in self.transactions if t.category.lower() == category.lower() and t.date[:7] == current_month))
            remaining = limit -  spent # already spent is negative
            percentage = (spent / limit * 100) if limit > 0 else 0

            status_color = Fore.GREEN if spent <= limit else Fore.RED
            status_text = "OK" if spent <= limit else "OVER BUDGET"

            # Build the perfectly aligned status line
            line = (
                f"  {category}:".ljust(30) + " " +
                f"Budget: Rs.{limit:>10.2f}".ljust(22) + "  |  " +
                f"Spent: Rs.{spent:>10.2f}".ljust(22) + " " +
                f"({percentage:.1f}%)".ljust(15) + "  |  " +
                status_color + f"{status_text}".ljust(18)
            )

            print(Fore.CYAN + "║" + Fore.WHITE + line + Fore.CYAN + " ║")

            if spent > limit:
                print(Fore.CYAN + "║" + Fore.WHITE + f"  ⚠️  Over by Rs.{abs(remaining):.2f}".ljust(120) + Fore.CYAN + "║")
                print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
            else:
                print(Fore.CYAN + "║" + Fore.WHITE + f"  Remaining: Rs.{remaining:.2f}".ljust(120) + Fore.CYAN + "║")
                print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        
    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def total_balance(self):
        return sum([transaction.amount for transaction in self.transactions]) 
    
    def list_all(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + f"  No transactions yet.".ljust(120) + Fore.CYAN + "║")
            return
        
        print(Fore.CYAN + "║" + Fore.WHITE + " S.NO. Date       Category             Amount        Description".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        for number, t in enumerate(self.transactions, 1):
            print(Fore.CYAN + "║" + Fore.WHITE + self._format_row(t, number).ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")


    def search_by_category(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + "  No transactions to search.".ljust(120) + Fore.CYAN + "║")
            return
        
        search_term = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter category to search: ".ljust(120) + Fore.CYAN + "║").strip()
        if not search_term:
            print(Fore.CYAN + "║" + Fore.RED + "  ❌ Search term cannot be empty.".ljust(118) + Fore.CYAN + " ║")
            return

        # filter transactions with List comprehension
        results = [t for t in self.transactions if t.category.lower() == search_term.lower()]

        if not results:
            print(Fore.CYAN + "║" + Fore.RED + f"  No transactions found for '{search_term}'.".ljust(120) + Fore.CYAN + "║")
            return
        
        total = sum(t.amount for t in results) # we call this as generator expression

        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.YELLOW + f"  SEARCH: {search_term.upper()}".center(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.WHITE + " S.NO. Date       Category             Amount        Description".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        for i, t in enumerate(results, 1):
            print(Fore.CYAN + "║" + Fore.WHITE + self._format_row(t, i).ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Found {len(results)} transaction(s) in Category Total: Rs.{total:.2f}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")

    def search_by_date_range(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + "  No transactions to search.".ljust(120) + Fore.CYAN + "║")
            return

        # Get start date with validation loop
        while True:
            start_raw = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter start date (YYYY-MM-DD): ".ljust(120) + Fore.CYAN + "║").strip()
            try:
                datetime.strptime(start_raw, "%Y-%m-%d") # validates format
                break
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid date. Use YYYY-MM-DD (e.g., 2026-05-01).".ljust(118) + Fore.CYAN + " ║")

        # Get end date with validation loop
        while True:
            end_raw = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter end date (YYYY-MM-DD): ".ljust(120) + Fore.CYAN + "║").strip()
            try:
                datetime.strptime(end_raw, "%Y-%m-%d")
                break
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid date. Use YYYY-MM-DD (e.g., 2026-05-31).".ljust(118) + Fore.CYAN + " ║")

        # Filter with list comprehension and string comparision
        results = [t for t in self.transactions if start_raw <= t.date <= end_raw]

        if not results:
            print(Fore.CYAN + "║" + Fore.RED + f"  No transactions between {start_raw} and {end_raw}.".ljust(120) + Fore.CYAN + "║")
            return

        total = sum(t.amount for t in results)

        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.YELLOW + f"  DATE RANGE: {start_raw} --> {end_raw}".center(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.WHITE + " S.NO. Date       Category             Amount        Description".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        for i, t in enumerate(results, 1):
            print(Fore.CYAN + "║" + Fore.WHITE + self._format_row(t, i).ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Found {len(results)} transaction(s)   Total: Rs.{total:.2f}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")




    def __str__(self):
        total_transactions = len(self.transactions)
        return (Fore.CYAN + "║" + Fore.WHITE+ f"  Finance Manager | {total_transactions} transactions | Total: ₹{self.total_balance()}".ljust(120) + Fore.CYAN + "║")

    def _format_row(self, t, number=None):
        """Return a string like ' 1. 2026-05-16 Food          Rs.  500.00  Luch at mess"""
        num_str = f"{number:>5}." if number is not None else "    "
        date_str = t.date
        cat_str = t.category[:20].ljust(20)        # max 20 chars, pad to 20
        amt_str = f"Rs.{t.amount:>10.2f}"          # right-aligned 10-wide
        # description: limit to remaining space (120 - box borders - fields)
        # We'll allocate 55 chars for description (leaving room for borders)
        desc_str = (t.description if t.description else "")[:55].ljust(55)
        return f"{num_str} {date_str} {cat_str} {amt_str} {desc_str}"
    
    def save_to_file(self):
        data = []
        for transaction in self.transactions:
            data.append(transaction.to_dict())
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(Fore.CYAN + "║ " + Fore.GREEN + f" 💾 Data saved to {self.filename}".ljust(118) + Fore.CYAN + "║")

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.transactions = []
            skipped_count = 0

            for item in data:
                try:
                    transaction = Transaction.from_dict(item)
                    self.transactions.append(transaction)
                except (ValueError, KeyError, TypeError):
                    skipped_count += 1
                    continue
            
            if skipped_count > 0:
                print(Fore.CYAN + "║" + Fore.YELLOW + f"  Warning: Skipped {skipped_count} invalid transactions.".ljust(118) + Fore.CYAN + " ║")

            print(Fore.CYAN + "║" + Fore.WHITE + f"  Loaded {len(self.transactions)} transactions from {self.filename}".ljust(120) + Fore.CYAN + "║")

        except FileNotFoundError:
            print(Fore.CYAN + "║" + Fore.WHITE + "  No save file found. Starting fresh.".ljust(120) + Fore.CYAN + "║")
            self.transactions = []
        except json.JSONDecodeError:
            print(Fore.CYAN + "║" + Fore.RED + "  Save file corrupted. Starting fresh.".ljust(118) + Fore.CYAN + " ║")
            self.transactions = []

    def monthly_summary(self, year_month):
        month_transactions = []
        total_income = 0
        total_expense = 0
        for transaction in self.transactions:
            if transaction.date.startswith(year_month):
                month_transactions.append(transaction)
                if transaction.amount > 0:
                    total_income += transaction.amount
                else:
                    total_expense += transaction.amount
        if not month_transactions:
            print(Fore.CYAN + "║" + Fore.RED + f"  No transactions found for this period.".ljust(120) + Fore.CYAN + "║")
            return
        net_amount = total_income + total_expense
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║ " + Fore.YELLOW + f"🌼 MONTHLY SUMMARY FOR {year_month} 🌼".center(117) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Total Income       :    ₹{total_income}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Total Expense      :    ₹{abs(total_expense)}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Net                :    ₹{net_amount}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.YELLOW + "  DETAILS:".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        number = 1
        for transaction in month_transactions:
            print(Fore.CYAN + "║" + Fore.WHITE + self._format_row(transaction, number).ljust(120) + Fore.CYAN + "║")
            number += 1
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
            
    def _save_data(self):
        self.save_to_file()
    
    def edit_transaction(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + "  No transactions to edit.".ljust(120) + Fore.CYAN + "║")
            return
        
        self.list_all()
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Enter a number between 1 and {len(self.transactions)}".ljust(120) + Fore.CYAN + "║")
        try:
            number = int(input(Fore.CYAN + "║" + Fore.WHITE+ "  Enter the transaction number to edit: ".ljust(120) + Fore.CYAN + "║"))
            index = number -1  # user sees 1-based, Python needs 0-based
        except ValueError:
            print(Fore.CYAN + "║" + Fore.WHITE+ " Please enter a valid number.".ljust(120) + Fore.CYAN + "║")
            return
 
        if index < 0 or index >= len(self.transactions):
            print(Fore.CYAN + "║" + Fore.WHITE+ " Please choose transaction within the transactions.".ljust(120) + Fore.CYAN + "║")
            return

        t = self.transactions[index]
        # IMPORTANT: 't' is NOT a copy. It is a direct reference to the object
        # inside self.transactions. Any change you make to t.amount will
        # automatically appear in self.transactions[index].amount as well.

        print(Fore.CYAN + "║" + Fore.WHITE+ f"  Current values:".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    Amount     : Rs.{t.amount:.2f}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    Category   : {t.category}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    Description: {t.description}".ljust(120) + Fore.CYAN + "║")

        print(Fore.CYAN + "║" + Fore.WHITE+ f"  What do you want to change?".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    1. Amount".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    2. Category".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"    3. Description".ljust(120) + Fore.CYAN + "║")

        field = input(Fore.CYAN + "║" + Fore.WHITE+ "  Enter choice (1/2/3): ".ljust(120) + Fore.CYAN + "║").strip()
    
        if field == "1":
            try:
                new_amount = float(input(Fore.CYAN + "║" + Fore.WHITE+ "  Enter new amount: ".ljust(120) + Fore.CYAN + "║"))
                t.amount = new_amount
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid amount. No changes made.".ljust(118) + Fore.CYAN + " ║")
                return
        elif field == "2":
            new_category = input(Fore.CYAN + "║" + Fore.WHITE+ "  Enter new category: ".strip().ljust(120) + Fore.CYAN + "║")
            if not new_category:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Category cannot be empty. No changes made.".ljust(118) + Fore.CYAN + " ║")
                return
            t.category = new_category
        elif field == "3":
            new_desc = input(Fore.CYAN + "║" + Fore.WHITE+ "  Enter new description (press Enter to clear): ".strip().ljust(120) + Fore.CYAN + "║")
            t.description = new_desc

        else:
            print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid choice. No changes made.".ljust(118) + Fore.CYAN + " ║")
            return
        
        self._save_data()
        print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Transaction updated and saved successfully.".ljust(120) + Fore.CYAN + " ║")

    def delete_transaction(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + " No transactions to delete.".ljust(120) + Fore.CYAN + "║")
            return 
        
        self.list_all()  # Show numberedlist so user can choose

        print(Fore.CYAN + "║" + Fore.WHITE + f"  Enter a number between 1 and {len(self.transactions)}".ljust(120) + Fore.CYAN + "║")
        try:
            number = int(input(Fore.CYAN + "║" + Fore.WHITE + "  Enter the transaction number to delete: ".ljust(120) + Fore.CYAN + "║"))
            index = number -1
        except ValueError:
            print(Fore.CYAN + "║" + Fore.RED + " ❌ Please enter a valid number.".ljust(118) + Fore.CYAN + "║")
            return
        
        if index < 0 or index >= len(self.transactions):
            print(Fore.CYAN + "║" + Fore.RED + "  ❌ That number is out of range.".ljust(118) + Fore.CYAN + " ║")
            return

        t = self.transactions[index]
        # Show what is about to be erased
        print(Fore.CYAN + "║" + Fore.WHITE + f"  You are about to delete:".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  {self._format_row(t)}".ljust(120) + Fore.CYAN + "║")

        confirm = input(Fore.CYAN + "║" + Fore.RED + "  Are you sure? Type 'yes' to confirm: ".lower().ljust(120) + Fore.CYAN + "║").strip().lower()

        if confirm == "yes":
            self.transactions.pop(index)  # this does the actua deletion
            self._save_data()              # persist immediately
            print(Fore.CYAN + "║" + Fore.GREEN + "  ✔️  Transaction deleted and saved.".ljust(120) + Fore.CYAN + " ║")
        else:
            print(Fore.CYAN + "║" + Fore.WHITE + "  Deletion cancelled. No changes made.".ljust(120) + Fore.CYAN + "║")

    def show_statistics(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + "  No data available for statistics.".ljust(120) + Fore.CYAN + "║")
            return

        count  = len(self.transactions)
        total = sum(t.amount for t in self.transactions) # generator expression
        average = total / count

        # Largest and smallest transactions (by amount)
        biggest = max(self.transactions, key=lambda t: t.amount)
        smallest = min(self.transactions, key=lambda t: t.amount)

        # Count how many times each category appears
        category_counts = {}
        for t in self.transactions:
            category_counts[t.category] = category_counts.get(t.category, 0) + 1
        most_used_category = max(category_counts, key=category_counts.get)

        # Total amount per category (to find highest-spending category)
        category_totals = {}
        for t in self.transactions: 
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

        highest_spending_category = (max(category_totals, key=category_totals.get))

        # Monthly totals to find most expensive month
        monthly_totals = {}
        for t in self.transactions:
            month = t.date[:7] # "YYYY-MM"
            monthly_totals[month] = monthly_totals.get(month, 0) + t.amount

        if monthly_totals:
            worst_month = max(monthly_totals, key=monthly_totals.get)
        else:
            worst_month = "N/A"

        # Display everything in our beautiful bordered style
    
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Total Transactions      : {count}".ljust(120)                                        + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Total Amount Spent      : Rs.{total:.2f}".ljust(120)                                 + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Average Per Transaction : Rs.{average:.2f}".ljust(120)                               + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " "                                                         + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Largest Expense         : Rs.{biggest.amount:.2f} ({biggest.category})".ljust(120)   + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Smallest Expense        : Rs.{smallest.amount:.2f} ({smallest.category})".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Most Used Category      : {most_used_category} ({category_counts[most_used_category]} times)".ljust(120)                + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Highest Spending Cat.   : {highest_spending_category} (Rs.{category_totals[highest_spending_category]:.2f})".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Most Expensive Month    : {worst_month} (Rs.{monthly_totals.get(worst_month, 0):.2f})".ljust(120)                       + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")

    def export_to_csv(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + "  No transactions to export.".ljust(120) + Fore.CYAN + "║")
            return
        
        # Build a filename with today's date so exports never overwrite
        today_str = datetime.today().strftime("%Y-%m-%d")
        filename = f"transactions_{today_str}.csv"

        # 'newline=""' is required for csv.writer on Windows.
        # Without it, an extra blank line appears between every row.
        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Write the header row: date, category, amount, description
            writer.writeheader()

            # Convert each Transaction object to a dict and write as a row
            for t in self.transactions:
                writer.writerow(t.to_dict())
        print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Exported {len(self.transactions)} transactions to '{filename}'".ljust(120) + Fore.CYAN + " ║")
        print(Fore.CYAN + "║" + Fore.WHITE + "  Open this file in Excel or Google Sheets.".ljust(120) + Fore.CYAN + "║")



def show_splash_screen():
    print(Fore.CYAN + "╔" + "═" * 120 + "╗")
    print(Fore.CYAN + "║ 🏵️" + Fore.YELLOW +  "💰 PERSONAL FINANCE 🏦 MANAGER v4.0 💰".center(112) + Fore.CYAN + "🏵️  ║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + "💻 DEVELOPED BY: GUVVALA VENKATA NARAYANA 💻".center(118) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + "🏫 RGUKT NUZVID | B-TECH N24~BATCH 🏫".center(118) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ 🔷" + Fore.MAGENTA +  "🅖 uaranteed 🅥 ault 🅝 ational 🅑 ank".center(114) + Fore.CYAN + "🔷 ║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")

def show_menu():
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.YELLOW + "🌼 MAIN MENU 🌼".center(117) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 1. " + Fore.GREEN           + "Add Income".ljust(115)            + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 2. " + Fore.RED             + "Add Expense".ljust(115)           + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 3. " + Fore.LIGHTCYAN_EX    + "View Balance".ljust(115)          + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 4. " + Fore.WHITE           + "View All Transactions".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 5. " + Fore.YELLOW          + "Search by Category".ljust(115)    + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 6. " + Fore.YELLOW          + "Search by Date Range".ljust(115)  + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 7. " + Fore.LIGHTYELLOW_EX  + "Save to File".ljust(115)          + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 8. " + Fore.LIGHTCYAN_EX    + "Monthly Summary".ljust(115)       + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 9. " + Fore.LIGHTBLUE_EX    + "Edit Transaction".ljust(115)      + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "10. " + Fore.MAGENTA         + "Delete Transaction".ljust(115)    + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "11. " + Fore.LIGHTMAGENTA_EX + "Statistics Dashboard".ljust(115)  + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "12. " + Fore.LIGHTYELLOW_EX  + "Set Budget".ljust(115)            + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "13. " + Fore.LIGHTYELLOW_EX  + "Check Budget Status".ljust(115)   + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "14. " + Fore.LIGHTGREEN_EX   + "Export to CSV".ljust(115)         + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "15. " + Fore.RED             + "Exit".ljust(115)                  + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")

if __name__ == "__main__":
    show_splash_screen()
    fm = FinanceManager()
    fm.load_from_file()
    print(fm)
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.LIGHTBLUE_EX + "💠 WELCOME TO RGUKT-IIIT 🦅 BANK NUZVID-BRANCH 💠".center(116) + Fore.CYAN + "║")

    while True:
        show_menu()
        choice = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter your choice(1-15): ".ljust(120) + Fore.CYAN + "║")
        if choice == "15":
            fm.save_to_file()
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "🙏 THANK YOU FOR USING RGUKT-IIIT BANK 🙏".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "║" + Fore.WHITE + "🪪  Your finances are safe with us. Have a great day! 🪪".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.GREEN + "💻 Developed by Guvvala Venkata Narayana | RGUKT Nuzvid 💻".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╚" + "═" * 120 + "╝")
            break

        elif choice == "14":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📤 EXPORT TO CSV 📤".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.export_to_csv()

        elif choice == "13":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📊 CHECK BUDGET STATUS 📊".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.check_budget_status()

        elif choice == "12":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "💰 SET BUDGET 💰".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.set_budget()

        elif choice == "11":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📈  STATISTICS DASHBOARD 📈 ".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.show_statistics()

        elif choice == "10":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║ " + Fore.YELLOW + "🗑️  DELETE TRANSACTION 🗑️".center(120) + Fore.CYAN + " ║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.delete_transaction()

        elif choice == "9":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║ " + Fore.YELLOW + "✏️  EDIT TRANSACTION ✏️".center(120) + Fore.CYAN + " ║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.edit_transaction()

        elif choice == "8":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║ " + Fore.YELLOW + "🗓️  MONTHLY SUMMARY 🗓️".center(120) + Fore.CYAN + " ║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            while True:
                try:
                    input_month = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter month in YYYY-MM format: ".ljust(120) + Fore.CYAN + "║").strip()
                    validate_date = datetime.strptime(input_month, "%Y-%m") # validate format
                    fm.monthly_summary(input_month)
                    break
                except ValueError:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  ❌ Invalid entry. Please ensure the year and month are correct(e.g., 2026-06).".ljust(118) + Fore.CYAN + " ║")
                    
        elif choice == "7":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "💾 SAVE TO FILE 💾".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.save_to_file()
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  THANK YOU FOR CHOOSINNG RUKT-NUZVID SECURE BANK.".ljust(120) + Fore.CYAN + "║")
            
        elif choice == "6":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📅 SEARCH BY DATE RANGE 📅".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.search_by_date_range()

        elif choice =="5":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "🔍 SEARCH BY CATEGORY 🔍".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.search_by_category()
        
        elif choice == "4":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📋 VIEW ALL TRANSACTIONS 📋".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.list_all()

        elif choice == "3":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📊 VIEW BALANCE 📊".center(118) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Current Balance       : ₹{fm.total_balance():.2f}".ljust(120) + Fore.CYAN + "║")

        elif choice == "2":
            # ADD EXPENSE
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ➖ ADD EXPENSE ➖".ljust(118) + Fore.CYAN + "║")
            # --- get amount ---
            while True:
                raw = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter amount: ".ljust(120) + Fore.CYAN + "║").strip()
                try:
                    amount = float(raw)
                    if amount <= 0:
                        print(Fore.CYAN + "║" + Fore.RED + "  ❌ Amount must be positive.".ljust(118) + Fore.CYAN + " ║")
                        continue
                    break
                except ValueError:
                    print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid number. Please enter digits only.".ljust(118) + Fore.CYAN + " ║")
            # --- get category ---
            while True:
                cat = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter category: ".ljust(120) + Fore.CYAN + "║").strip()
                if not cat or len(cat.strip()) < 3 :
                    print(Fore.CYAN + "║" + Fore.RED + "  ❌ Category must be at least 3 characters.".ljust(118) + Fore.CYAN + " ║")
                    continue
                break
            # ---description (optional) ---
            desc = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter description (optional): ".ljust(120) + Fore.CYAN + "║").strip()
            today = date.today().strftime("%Y-%m-%d")
            t = Transaction(-amount, cat, today, desc)
            fm.add_transaction(t)
            # --- success with one-line transaction ---
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Added: {t}".ljust(120) + Fore.CYAN + " ║")

        elif choice == "1":
            # ADD INCOME
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ➕ ADD INCOME ➕".ljust(118) + Fore.CYAN + "║")
            # --- get amount ---
            while True:
                raw = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter amount: ".ljust(120) + Fore.CYAN + "║").strip()
                try:
                    amount = float(raw)
                    if amount <= 0:
                        print(Fore.CYAN + "║" + Fore.RED + "  ❌ Amount must be positive.".ljust(118) + Fore.CYAN + " ║")
                        continue
                    break
                except ValueError:
                    print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid number. Please enter digits only.".ljust(118) + Fore.CYAN + " ║")
            # --- get category ---
            while True:
                cat = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter category: ".ljust(120) + Fore.CYAN + "║").strip()
                if not cat or len(cat.strip()) < 3:
                    print(Fore.CYAN + "║" + Fore.RED + "  ❌ Category must be at least 3 characters.".ljust(118) + Fore.CYAN + " ║")
                    continue
                break
            # ---description (optional) ---
            desc = input(Fore.CYAN + "║" + Fore.WHITE + "  Enter description (optional): ".ljust(120) + Fore.CYAN + "║").strip()
            today = date.today().strftime("%Y-%m-%d")
            t = Transaction(amount, cat, today, desc)
            fm.add_transaction(t)
            # --- success with one-line transaction ---
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Added: {t}".ljust(120) + Fore.CYAN + " ║")

        else:
            print(Fore.CYAN + "║" + Fore.RED+ f"  🙅 Invalid Choice.".ljust(118) + Fore.CYAN + " ║")
