## PERSONAL FINANCE MANAGER CLI

A command-line personal finance tracking application built in Python.
Track your income and expenses, view monthly summaries, and manage
your financial records - all from the terminal.

---
## Features
-  Add income and expense transactions with amount, category, and description
-  View all transactions in a color-coded, bordered display
-  Monthly summary showing total spending per month
-  Data persistence using JSON - your data saves between sessions
-  Clean, formatted CLI interface using the colorama library

---
### Project Structure
Project1_Finance_Manager/

 |
 ├── main.py                               #  Current version (v2.0) - full featured CLI
 ├── main_v01.py                           #  v0.1 - procedural approach, no data saving
 ├── main_v1.py                            #  v1.0 - OOP with JSON persistence, no colors
 ├── data.json                             #  Auto-generated file storing your transactions
 ├── EXPLANATION.md                        #  Plain-English explanation of every major concept
 └── README.md                             #  This file

---
## Requirements

-  Python 3.8 or above
-  colorama library

Install colorama by running:
pip install colorama

---
## How to Run 
python main.py

---
## Version History

| Version | File        | What Changed                                           |
| ------- | ----------- | ------------------------------------------------------ |
| v0.1    | main_v01.py | Procedural design, in-memory list, no saving           |
| v1.0    | main_v1.py  | OOP introduced, JSON saving added                      |
| v2.0    | main.py     | Colorized interface, bordered display, monthly summary |

---
## Understanding the Code

For a complete plain-English explanation of every concept used 
in this project - including what classes are, how JSON saving works, 
and how the program loads your data at startup - read the 
[EXPLANATION.md](EXPLANATION.md) file.

---
## What I learned

Building this project taught me how to design Python classes,
persist data using JSON, handle user input safely with try/except,
and structure a project that grows through multiple versions.

---
## Author

**Guvvala Venkata Narayana**
B.Tech  at RAJIV GANDHI UNIVERSITY OF KNOWLEDGE TECHNOLOGIES | IIIT Nuzvid
GitHub: [https://github.com/Venkatanarayana7](https://github.com/Venkatanarayana7)

---
*Build during Summer 2026 as part of an independent Python learning program.*



