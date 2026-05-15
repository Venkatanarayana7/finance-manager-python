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
        for transaction in self.transactions:
            print(Fore.CYAN + "║" + Fore.WHITE + f"  {transaction}".ljust(120) + Fore.CYAN + "║")

    def list_by_category(self, category):
        for transaction in self.transactions:
            if transaction.category == category:
                print(Fore.CYAN + "║" + Fore.WHITE + f"  {transaction}".ljust(120) + Fore.CYAN + "║")

    def __str__(self):
        total_transactions = len(self.transactions)
        return (Fore.CYAN + "║" + Fore.WHITE+ f"  Finance Manager | {total_transactions} transactions | Total: ₹{self.total_balance()}".ljust(120) + Fore.CYAN + "║")

    def save_to_file(self, filename):
        data  = []
        for transaction in self.transactions:
            data.append(transaction.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(Fore.CYAN + "║" + Fore.WHITE+ f"  Saved {len(self.transactions)} transactions to {filename}.".ljust(120) + Fore.CYAN + "║")

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
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        print(Fore.CYAN + "║" + Fore.YELLOW + "  DETAILS:".ljust(120) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 120 + "╣")
        for transaction in month_transactions:
            print(Fore.CYAN + "║" + Fore.WHITE + f"  {transaction}".ljust(120) + Fore.CYAN + "║")


def show_splash_screen():
    print(Fore.CYAN + "╔" + "═" * 120 + "╗")
    print(Fore.CYAN + "║ 🏵️" + Fore.YELLOW +  "💰 PERSONAL FINANCE 🏦 MANAGER v2.0 💰".center(112) + Fore.CYAN + "🏵️  ║")
    print(Fore.CYAN + "╠" + "═" * 120 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + "💻 DEVELOPED BY: GUVVALA VENKATA NARAYANA 💻".center(118) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.GREEN + "🏫 RGUKT NUZVID | AI & ML N24~CS30 🏫".center(118) + Fore.CYAN + "║")
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
    print(Fore.CYAN + "║ " + Fore.WHITE + " 8. " + Fore.RED + "Exit".ljust(115) + Fore.CYAN + "║")
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
        choice = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter your choic(1-8): ".ljust(120) + Fore.CYAN + "║").strip()
        if choice == "8":
            fm.save_to_file("transactions.json")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Goodbye.".ljust(120) + Fore.CYAN + "║")
            print(Fore.CYAN + "╚" + "═" * 120 + "╝")
            break

        elif choice == "7":
            while True:
                try:
                    input_month = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter month in YYYY-MM format: ".ljust(120) + Fore.CYAN + "║").strip()
                    validate_date = datetime.strptime(input_month, "%Y-%m") # validate format
                    fm.monthly_summary(input_month)
                    break
                except ValueError:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  ❌ Invalid entry. Please ensure the year and month are correct(e.g., 2026-06).".ljust(118) + Fore.CYAN + " ║")
                    
        elif choice == "6":
            fm.save_to_file("transactions.json")
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  THANK YOU FOR CHOOSINNG RUKT-NUZVID SECURE BANK.".ljust(120) + Fore.CYAN + "║")
            

        elif choice =="5":
            cat = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter category to filter: ".ljust(120) + Fore.CYAN + "║").strip()
            fm.list_by_category(cat)
        
        elif choice == "4":
            fm.list_all()

        elif choice == "3":
            print(Fore.CYAN + "║" + Fore.WHITE+ f"  Current Balance: ₹{fm.total_balance():.2f}".ljust(120) + Fore.CYAN + "║")

        elif choice == "2":
            try:
                amount = float(input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter amount (will be deducted)".ljust(120) + Fore.CYAN + "║"))
                if amount <= 0:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  Amount must be positive.".ljust(120) + Fore.CYAN + "║")
                    continue

                category = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter category: ".ljust(120) + Fore.CYAN + "║").strip()
                if not category:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  Category required.".ljust(120) + Fore.CYAN + "║")
                    continue

                desc = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter description (optional): ".ljust(120) + Fore.CYAN + "║").strip()
                today = date.today().strftime("%Y-%m-%d")
                t = Transaction(-amount, category, today, desc)
                fm.add_transaction(t)
                print(Fore.CYAN + "║" + Fore.WHITE+ f"  ✔️  Expense added Successfully!".ljust(120) + Fore.CYAN + " ║")
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED+ f"  ❌ Invalid amount. Please enter a number.".ljust(118) + Fore.CYAN + " ║")
    
        elif choice == "1":
            try:
                amount = float(input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter amount: ".ljust(120) + Fore.CYAN + "║"))
                if amount <= 0:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  Amount must be positive.".ljust(120) + Fore.CYAN + "║")
                    continue
                category = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter category: ".ljust(120) + Fore.CYAN + "║").strip()
                if not category:
                    print(Fore.CYAN + "║" + Fore.WHITE+ f"  Category required.".ljust(120) + Fore.CYAN + "║")
                    continue
                desc = input(Fore.CYAN + "║" + Fore.WHITE+ f"  Enter description (optional): ".ljust(120) + Fore.CYAN + "║").strip()
                today = date.today().strftime("%Y-%m-%d")
                t = Transaction(amount, category, today, desc)
                fm.add_transaction(t)
                print(Fore.CYAN + "║" + Fore.WHITE+ f"  ✔️  Income added Successfully!".ljust(120) + Fore.CYAN + " ║")
            except ValueError:
                print(Fore.CYAN + "║" + Fore.RED+ f"  ❌ Invalid amount.Please enter a number.".ljust(118) + Fore.CYAN + " ║")
        else:
            print(Fore.CYAN + "║" + Fore.RED+ f"  🙅 Invalid Choice.".ljust(118) + Fore.CYAN + " ║")
