import json
from datetime import date, datetime
from colorama import init, Fore, Style
init(autoreset=True)
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
    def __init__(self):
        self.transactions = []
        
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

    def list_by_category(self, category):
        number = 1
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.YELLOW + f"LIST BY {category.upper()} CATEGORY".center(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.WHITE + " S.NO. Date       Category             Amount        Description".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        for transaction in self.transactions:
            if transaction.category.lower() == category.lower():
                print(Fore.CYAN + "║" + Fore.WHITE + self._format_row(transaction, number).ljust(120) + Fore.CYAN + "║")
                number += 1
        print(Fore.CYAN + "║" + Fore.WHITE + " " + "-"*118 + Fore.WHITE + " " + Fore.CYAN + "║")
        if number == 1:
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  No transactions found for {category} category.".ljust(120) + Fore.CYAN + "║")

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
    

    def save_to_file(self, filename):
        data  = []
        for transaction in self.transactions:
            data.append(transaction.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(Fore.CYAN + "║ " + Fore.GREEN + " 💾 Data saved to transactions.json".ljust(118) + Fore.CYAN + "║")
    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.transactions = []
            skipped_count = 0

            for item in data:
                try:
                    transaction = Transaction.from_dict(item)
                    self.transactions.append(transaction)
                except( ValueError, KeyError, TypeError) as e:
                    skipped_count += 1
                    continue
            
            if skipped_count > 0:
                print(Fore.CYAN + "║" + Fore.WHITE+ f"  Warning: Skipped {skipped_count} invalid transactions from old format".ljust(120) + Fore.CYAN + "║")

            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Loaded {len(self.transactions)} transactions from {filename}".ljust(120) + Fore.CYAN + "║")

        except FileNotFoundError:
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  No save file found. Starting fresh.".ljust(120) + Fore.CYAN + "║")
            self.transactions = []
        except json.JSONDecodeError:
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Save file corrupted. Starting fresh".ljust(120) + Fore.CYAN + "║")
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
        self.save_to_file("transactions.json")
    
    def edit_transaction(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.WHITE+ "No transactions to edit.".ljust(120) + Fore.CYAN + "║")
            return
        
        self.list_all()
        print(Fore.CYAN + "║" + Fore.WHITE + f"  Enter a number between 1 and {len(self.transactions)}".ljust(120) + Fore.CYAN + "║")
        try:
            number = int(input(Fore.CYAN + "║" + Fore.WHITE+ "Enter the transaction number to edit: ".ljust(120) + Fore.CYAN + "║"))
            index = number -1  # user sees 1-based, Python needs 0-based
        except ValueError:
            print(Fore.CYAN + "║" + Fore.WHITE+ "Please enter a valid number.".ljust(120) + Fore.CYAN + "║")
            return
 
        if index < 0 or index >= len(self.transactions):
            print(Fore.CYAN + "║" + Fore.WHITE+ "Please choose transaction within the transactions.".ljust(120) + Fore.CYAN + " ║")
            return

        t = self.transactions[index]
        # IMPORTANT: 't' is NOT a copy. It is a direct reference to the object
        # inside self.transactions. Any change you make to t.amount will
        # automatically appear in self.transactions[index].amount as well.

        print(Fore.CYAN + "║" + Fore.WHITE+ f"Current values:".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  Amount     : Rs.{t.amount:.2f}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  Category   : {t.category}".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  Description: {t.description}".ljust(120) + Fore.CYAN + "║")

        print(Fore.CYAN + "║" + Fore.WHITE+ f"What do you want to change?".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  1. Amount".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  2. Category".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  3. Description".ljust(120) + Fore.CYAN + "║")

        field = input(Fore.CYAN + "║" + Fore.WHITE+ "Enter choice (1/2/3): ".strip().ljust(120) + Fore.CYAN + "║")
    
        if field == "1":
            try:
                new_amount = float(input(Fore.CYAN + "║" + Fore.WHITE+ "Enter new amount: ".ljust(120) + Fore.CYAN + "║"))
                t.amount = new_amount
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid amount. No changes made.".ljust(118) + Fore.CYAN + " ║")
                return
        elif field == "2":
            new_category = input(Fore.CYAN + "║" + Fore.WHITE+ "Enter new category: ".strip().ljust(120) + Fore.CYAN + "║")
            if not new_category:
                print(Fore.CYAN + "║" + Fore.RED + "  ❌ Category cannot be empty. No changes made.".ljust(118) + Fore.CYAN + " ║")
                return
            t.category = new_category
        elif field == "3":
            new_desc = input(Fore.CYAN + "║" + Fore.WHITE+ "Enter new description (press Enter to clear): ".strip().ljust(120) + Fore.CYAN + "║")
            t.description = new_desc

        else:
            print(Fore.CYAN + "║" + Fore.RED + "  ❌ Invalid choice. No changes made.".ljust(118) + Fore.CYAN + " ║")
            return
        
        self._save_data()
        print(Fore.CYAN + "║" + Fore.GREEN + f"  ✔️  Transaction updated and saved successfully.".ljust(120) + Fore.CYAN + " ║")

    def delete_transaction(self):
        if not self.transactions:
            print(Fore.CYAN + "║" + Fore.RED + " No transactions to delete.".ljust(118) + Fore.CYAN + " ║")
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
        print(Fore.CYAN + "║" + Fore.WHITE + f"    {self._format_row(t)}".ljust(120) + Fore.CYAN + "║")

        confirm = input(Fore.CYAN + "║" + Fore.RED + "  Are you sure? Type 'yes' to confirm: ".lower().ljust(120) + Fore.CYAN + "║").strip().lower()

        if confirm == "yes":
            self.transactions.pop(index)  # this does the actua deletion
            self._save_data()              # persist immediately
            print(Fore.CYAN + "║" + Fore.GREEN + "  ✔️  Transaction deleted and saved.".ljust(120) + Fore.CYAN + " ║")
        else:
            print(Fore.CYAN + "║" + Fore.WHITE + "  Deletion cancelled. No changes made.".ljust(120) + Fore.CYAN + "║")

def show_splash_screen():
    print(Fore.CYAN + "╔" + "═" * 120 + "╗")
    print(Fore.CYAN + "║ 🏵️" + Fore.YELLOW +  "💰 PERSONAL FINANCE 🏦 MANAGER v3.0 💰".center(112) + Fore.CYAN + "🏵️  ║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + "💻 DEVELOPED BY: GUVVALA VENKATA NARAYANA 💻".center(118) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + "🏫 RGUKT NUZVID | B-TECH N24~CS30 🏫".center(118) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.MAGENTA +  "🅖 uaranteed 🅥 ault 🅝 ational 🅑 ank".center(120) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")

def show_menu():
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.YELLOW + "🌼 MAIN MENU 🌼".center(117) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 1. " + Fore.GREEN + "Add Income".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 2. " + Fore.RED + "Add Expense".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 3. " + Fore.BLUE + "View Balance".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 4. " + Fore.MAGENTA + "View All Transactions".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 5. " + Fore.YELLOW + "View by Category".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 6. " + Fore.GREEN + "Save to File".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 7. " + Fore.GREEN + "Monthly Summary".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 8. " + Fore.GREEN + "Edit Transaction".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + " 9. " + Fore.GREEN + "Delete Transaction".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "10. " + Fore.RED + "Exit".ljust(115) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")

if __name__ == "__main__":
    show_splash_screen()
    fm = FinanceManager()
    fm.load_from_file("transactions.json")
    print(fm)
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║ " + Fore.LIGHTBLUE_EX + "💠 WELCOME TO RGUKT-IIIT 🦅 BANK NUZVID-BRANCH 💠".center(116) + Fore.CYAN + "║")

    while True:
        show_menu()
        choice = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter your choice(1-10): ".ljust(120) + Fore.CYAN + "║")
        if choice == "10":
            fm.save_to_file("transactions.json")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Goodbye.".ljust(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╚" + "═" * 120 + "╝")
            break
        
        elif choice == "9":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "DELETE TRANSACTION".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.delete_transaction()

        elif choice == "8":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "EDIT TRANSACTION".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.edit_transaction()

        elif choice == "7":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "MONTHLY SUMMARY".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            while True:
                try:
                    input_month = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter month in YYYY-MM format: ".ljust(120) + Fore.CYAN + "║").strip()
                    validate_date = datetime.strptime(input_month, "%Y-%m") # validate format
                    fm.monthly_summary(input_month)
                    break
                except ValueError:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  ❌ Invalid entry. Please ensure the year and month are correct(e.g., 2026-06).".ljust(118) + Fore.CYAN + " ║")
                    
        elif choice == "6":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "SAVE TO FILE".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.save_to_file("transactions.json")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  THANK YOU FOR CHOOSINNG RUKT-NUZVID SECURE BANK.".ljust(120) + Fore.CYAN + "║")
            

        elif choice =="5":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "VIEW BY CATEGORY".center(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            cat = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter category to filter: ".ljust(120) + Fore.CYAN + "║").strip()
            fm.list_by_category(cat)
        
        elif choice == "4":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📋 VIEW ALL TRANSACTIONS".center(118) + Fore.CYAN + " ║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            fm.list_all()

        elif choice == "3":
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.YELLOW + "📊 VIEW BALANCE".center(118) + Fore.CYAN + " ║")
            print(Fore.CYAN + "╠" + "═" * 120 + "╣")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Current Balance       : ₹{fm.total_balance():.2f}".ljust(120) + Fore.CYAN + "║")

        elif choice == "2":
            # ADD EXPENSE
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ➖ ADD EXPENSE".ljust(118) + Fore.CYAN + " ║")
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
            print(Fore.CYAN + "║" + Fore.GREEN + f"  ➕ ADD INCOME".ljust(118) + Fore.CYAN + " ║")
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
