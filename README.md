# 💰 Personal Finance Manager v4.0 💰

A full‑featured command‑line personal finance tracker built from scratch in Python with OOP architecture, JSON persistence, budget tracking, statistical analysis, and a colorized terminal UI using box‑drawing characters.

**Developer:** Guvvala Venkata Narayana  
**Institution:** RGUKT Nuzvid · B.Tech (2026~2030) · N24 Batch  
**Built During:** Summer 2026 · 12 focused working days  
**Language:** Python 3.10+ · Tested on Ubuntu 24.04  

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | ➕ Add Income | Record income with category and optional description, date auto-set to today |
| 2 | ➖ Add Expense | Record expenses stored as negative amount, full input validation |
| 3 | 💰 View Balance | Live net balance calculated from all stored transactions |
| 4 | 📋 View All | Numbered, column-aligned table of every transaction |
| 5 | 🔍 Search by Category | Case-insensitive filter showing matching transactions and category total |
| 6 | 📅 Search by Date Range | Filter transactions between two validated YYYY-MM-DD dates |
| 7 | 💾 Save to File | Manually persist data to JSON (also auto-saves on exit) |
| 8 | 📆 Monthly Summary | Income/expense breakdown and full listing for any YYYY-MM period |
| 9 | ✏️ Edit Transaction | Modify amount, category, or description of any existing entry |
| 10 | 🗑️ Delete Transaction | Remove any transaction with a typed confirmation prompt |
| 11 | 📊 Statistics Dashboard | Count, total, average, largest/smallest, top categories, worst month |
| 12 | 🎯 Set Budget | Monthly spending limit per category, stored in a separate file |
| 13 | ✅ Check Budget Status | Live budget vs. actual with over-budget warnings in red |
| 14 | 📤 Export to CSV | Date-stamped CSV compatible with Excel and Google Sheets |

---

## How to Run

```bash
git clone https://github.com/Venkatanarayana7/finance-manager-python.git
cd finance-manager-python
pip install colorama
python main.py
```

The program will automatically create `finance_data.json` and `budgets.json` in the same folder as `main.py` on first run. You do not need to create these manually.
---

## Project Structure

```
Project1_Finance_Manager/
├── main.py                      ← All source code (single file)
├── finance_data.json            ← Auto-generated: transaction storage
├── budgets.json                 ← Auto-generated: monthly budget settings
├── transactions_YYYY-MM-DD.csv  ← Generated when you use Export to CSV
├── README.md                    ← This file
└── EXPLANATION.md               ← Deep technical Q&A documentation
```

---

## Architecture

The application is built around two classes with clearly separated responsibilities.

```
Transaction
│
├── __init__(amount, category, date, description)
│     Stores one financial record. Income is positive, expense is negative.
│
├── __str__()
│     Returns a formatted human-readable string for terminal display.
│
├── to_dict()
│     Converts the object to a Python dictionary for JSON serialization.
│
└── from_dict(cls, data)   ← @classmethod
      Rebuilds a Transaction from a dictionary (e.g., loaded from file).
      Validates required keys before constructing; raises ValueError if missing.

FinanceManager
│
├── Data stored on the object:
│     self.transactions  → list of Transaction objects
│     self.budgets       → dict mapping category names to monthly limits
│     self.filename      → absolute path to finance_data.json
│     self.budget_file   → absolute path to budgets.json
│
├── Persistence:
│     load_from_file()   → reads JSON, rebuilds Transaction objects
│     save_to_file()     → serializes all transactions to JSON
│     _load_budgets()    → reads budgets.json on startup
│     _save_budgets()    → writes budgets.json whenever a budget changes
│
├── CRUD operations:
│     add_transaction()      → append to list
│     edit_transaction()     → modify in-place via direct object reference
│     delete_transaction()   → remove with list.pop(index)
│
├── Views:
│     list_all()             → formatted numbered table
│     monthly_summary()      → income/expense breakdown per month
│     show_statistics()      → full analytics dashboard
│
├── Search:
│     search_by_category()   → case-insensitive category filter
│     search_by_date_range() → date string comparison (YYYY-MM-DD sorts correctly)
│
└── Budget:
      set_budget()           → store category limit in self.budgets
      check_budget_status()  → compare monthly actual vs. limit
```

---

## Key Technical Concepts

**Object-Oriented Programming.**: Two classes with clear responsibilities, Transaction` knows how to represent and serialize itself; `FinanceManager` knows how to manage a collection of them. Neither class knows about terminal colors or user input, which is handled by the functions and main block outside the classes.

**JSON Serialization with Backwards Compatibility.**: `to_dict()` converts a Transaction to a plain Python dictionary. `from_dict()` reverses this. Critically, `from_dict()` uses `data.get("description", "")` rather than `data["description"]`, meaning old saved files without a description field load correctly instead of raising a `KeyError`. This is called backwards compatibility.

**Script-Directory-Relative File Paths.**: The line `script_dir = os.path.dirname(os.path.abspath(__file__))` finds the absolute path of the folder where `main.py` lives. All data files are stored relative to this directory, not relative to whatever folder the terminal is currently in. This means the program finds its data correctly regardless of where you run it from.

**Separation of Concerns in Data Storage.**: Transactions live in `finance_data.json`. Budgets live in `budgets.json`. This means a bug in budget-related code cannot corrupt transaction data, and vice versa. Each file has exactly one responsibility.

**Lambda Functions for Sorting.**: The Statistics Dashboard uses `max(self.transactions, key=lambda t: t.amount)` to find the transaction with the highest amount. The `lambda t: t.amount` tells Python what attribute to compare when evaluating "largest" without this, Python would not know how to compare two Transaction objects.

**Input Validation Pattern.**: Every user input that requires a number uses a `while True:` loop with `try/except ValueError`, breaking only when valid input is received. Every string input that must be non-empty is checked with an `if not value:` guard. The program never crashes from user input.
---

## 📝 Version History


| Version | Description |
| :--- | :--- |
| **v0.1** | Procedural script, in‑memory list, no saving |
| **v1.0** | OOP with Transaction & FinanceManager classes, JSON persistence |
| **v2.1** | Colorized CLI, box‑drawing borders, monthly summary |
| **v2.2** | Edit & Delete transactions with confirmation |
| **v2.3** | Category/Date search, Statistics dashboard |
| **v2.4** | Budget tracker with separate budgets.json |
| **v3.0** | CSV export, script‑relative paths |
| **v4.0** | Full visual polish, symmetric headers, menu emojis, final documentation |

---

## 📖 What I Learned

- Designing Python classes and understanding `self`, `__init__`, `__str__`, `@classmethod`
- JSON serialization/deserialization and file I/O with `with` contexts
- List comprehensions, generator expressions, and lambda functions
- Building robust CLI interfaces with infinite loops, input validation, and `colorama`
- Using `os.path` to make programs location‑independent
- Version control discipline, commit messages that tell a story

---

## 👤 About the Developer

I’m *Guvvala Venkata Narayana*, a first‑year B.Tech student at RGUKT Nuzvid. This project was part of my self‑designed Summer Ark 2026 series, five projects to build real engineering skills before my first semester begins. I believe in learning by building, and every line in this repository was written with that philosophy.

- **GitHub**: [VENKATANARAYANA7](https://github.com/Venkatanarayana7)
- **LinkedIn**: [VENKATA NARAYANA GUVVALA](https://www.linkedin.com/in/venkata-narayana-guvvala-9a568b376/)

_Built with discipline during Summer 2026 · Python 3.10.12 · colorama_

