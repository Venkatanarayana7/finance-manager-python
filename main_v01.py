# ==============================================================
# Personal Finance Manager - Version 0.1
# Author: Guvvala Venkata Narayana
# Date: May 2025
#
# This is the very first version of this project.
# It uses simple FUNCTIONS (not classes) to organize code.
# Data is stored in a plain Python LIST of dictionaries.
# When the program closes, ALL data is lost (no file saving yet).
# This version's purpose: prove the core idea works.
# ==============================================================

import datetime # We need this to get today's date automatically

# This is our "database" for now - just a Python list that lives
# in memory while the program is running. When we close the program,
# this list disappears. We fix that in v1.0 with JSON file saving.
transactions = []

def add_transaction():
    """
    This function asks the user for transaction details
    and adds a new dictionary entry to our transactoins list.
    A dictionary here acts like a simple record: {key: value, key: value...}
    """
    # We use try/except because if the user types "abc" instead of a number,
    # float("abc") would crash the program. try/except catches that crash.
    try:
        amount = float(input("Enter amount (e.g. 150.50): "))
    except ValueError:
        print("ERROR: Amount must be a number. Please try again.")
        return # 'return' exits the function early if input is bad
    category = input("Enter category (e.g. Food, Travel, Book): ").strip()
    # .strip() removes any accidental spaces the user might type beofre/after

    if not category: # if the user just pressed Enter without typing anything
        print("ERROR: Category cannot be empty.")
        return
    
    description = input("Enter a short description (press Enter to skip): ").strip()

    # datetime.date.today() gives us today's date as a date object.
    # .strftime("%Y-%m-%d") fromats it as a string like "2026-05-10".
    # We store dates as strings so they are easy to save and display.
    today = datetime.date.today().strftime("%Y-%m-%d")

    # A dictionary is like a labeled box. Each key is a label, each value is the content.
    # We create one dictionary per transaction.
    transaction = {
        "amount": amount,
        "category": category,
        "date": today,
        "description": description
    }

    transactions.append(transaction) # add this new record to our list
    print(f"\nSuccess! Added: {category} -Rs.{amount:.2f} on {today}")
    # The :.2f in the f-string means "format this float with exactly 2 decimal places"

def view_all_transactions():
    """ 
    This function loops through our transactions list and prints each one.
    It also calculates the running total at the end.
    """
    if not transactions: # Python treats an empty list as False
        print("\nNo transactions recorded yet. Add one first!")
        return
    
    print("\n" + "=" * 45)
    print("      ALL TRANSACTIONS")
    print("=" * 45)

    total = 0
    for index, t in enumerate(transactions, start=1):
        # enumerate() gives us both the index number AND the item at each step.
        # start=1 means we count from 1, not 0, so the user sees "1, 2, 3..."
        print(f"{index}. [{t['date']}] {t['category']:<15} Rs.{t['amount']:>8.2f}")
        print(f"   Description: {t['description'] or 'None'}")
        # The 'or' here means: if description is empty string, show "None" instead
        print("-" * 45)
        total+= t['amount']

    print(f"\nTOTAL SPENT: Rs.{total:.2f}")
    print("=" * 45)

def show_menu():
    """Prints the main menu. Kept separate so we can all it repeatedly."""
    print("\n" + "="*35)
    print("   PERSONAL FINANCE MANAGER v0.1")
    print("=" * 35)
    print(" 1. Add a Transaction")
    print(" 2. View All Transactions")
    print(" 3. Exit Program")
    print("=" * 35)

def main():
    """
    This is the entry point - the main loop of the program.
    It keeps running until the user chooses to exit.
    'while True' means 'keep looping forever until we explicitly break out'.
    """
    print("Welcome to Personal Fianance Manager!")
    print("NOTE: Data will be lost when you close this program.")
    print("      (We fix this in the next version!)")

    while True:
        show_menu()
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_all_transactions()
        elif choice == "3":
            print("\nGoodbye! See you next tiem.")
            break # 'break' exits the while Ture loop completely
        else:
            print("Invalid choice. Please enter only 1, 2, or 3.")

# This line means: "Only run main() if this file is executed directly.
# If another file imports this file, do NOT run main() automatically."
# It is a professional Python convention you should always include.
if __name__ == '__main__':
    main()
    
