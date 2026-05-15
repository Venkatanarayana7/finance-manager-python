# EXPLANATION.md – Finance Manager CLI Project

### Question 1: What problem does this project solve, and why does that problem matter to a real person?

This project solves the everyday struggle of keeping track of money, all the money coming in and going out.

Instead of messy notebooks or forgetting where the money went, a person can just type a few commands and instantly see their income, 
expenses, and a clear summary.

It matters because real people, especially those with many daily transactions, easily lose sight of their spending and saving. Having a quick, organized tool right in the terminal removes that confusion and helps anyone stay in control of their finances.

---

### Question 2: A friend who has never coded before asks you: "What is a class, and why did you use one in this project instead of just using functions?" How do you explain it in simple, everyday language?

A class is like a blueprint. Imagine you are building many similar houses – you use the same master plan but change the colour or size for each one.

In Python, a class is that master plan, and each actual house you build from it is called an “object”.  

I used a class for `Transaction` because every transaction has the same structure (amount, category, date, type), and I want each transaction to carry its own data inside itself.  

If I used only functions, I would have to pass that data around over and over again. With a class, I set the data once when I create the object, and then all the methods inside the class can reach it using `self`, much cleaner and less repetitive.

---

### Question 3: When the program starts, how does it find and load your old transaction data? Walk through the steps — from opening the program to seeing your saved transactions - in your own words.

When the program runs, the first thing that happens is the `main()` function is called. That creates a `FinanceManager` object, and as soon as that object is born, its `__init__` method runs automatically.  

Inside `__init__`, it calls _load_data() method that looks for a JSON file on the disk. 

If the file exists, the program reads it, converts the stored dictionaries into real `Transaction` objects using `from_dict()`, and loads them into a list – so all past entries are ready to use.  

If the file doesn’t exist yet, it simply starts with an empty list and waits to add the first transaction.

---

### Question 4: Why do you use JSON to save data, and not just a plain text file or a Word document?

Plain text files and Word documents treat everything as just words and formatting - they don’t understand that a number should stay a number or that a list should keep its shape.  

JSON, on the other hand, understands basic data types like numbers, strings, booleans, lists, and dictionaries – exactly the building blocks I need.  

When I save with JSON, the structure (like “amount = 50.0”) is preserved, so when I load it back, Python can turn it into a real number automatically, without JSON i have to guess and convert every piece manually.  

It’s light, human-readable, and Python’s built-in `json` module makes saving and loading almost effortless.

---

### Question 5: The `to_dict()` and `from_dict()` methods exist as a pair. Why are both of them necessary? What would break if you removed one of them?

These two methods are translators between the Python world and the JSON world. 
 
`to_dict()` takes a living `Transaction` object and turns it into a plain Python dictionary, because JSON can only store simple things like dicts, lists, and numbers – it cannot store a whole Python object directly.  

Then `json.dump` takes that dictionary and writes it to the file.  

`from_dict()` does the opposite: when we read the JSON file, we get back a dictionary, and that method rebuilds a real `Transaction` object from it, so we can use the object’s helpful methods.  

If I removed `to_dict()`, saving would fail because the program wouldn’t know how to convert an object into something JSON can handle.

If I removed `from_dict()`, loading would give me raw dictionaries, and I would lose all the behavior that makes a `Transaction` works.

---

### Question 6: What does the line `if __name__ == "__main__":` mean, and what would happen if you removed it?

This line is Python’s way of asking, “Am I being run directly, or am I being imported into another file?”  

If I run the file directly, Python sets a special variable `__name__` to `"__main__"`, and the condition becomes true - so it calls `main()` and starts the program.  

If someone else imports my file to use a function from it, `__name__` will be the file’s actual name, not `"__main__"`, so `main()` will not run automatically and mess up their code.  

Without this guard, every time someone imported my file, the whole finance manager would start running, printing menus and asking for input – which is definitely not what they want. It’s a simple safety switch that every Python project should have.

---

### Question 7: What is the single biggest thing you learned while building this project - not a fact or a concept, but something about yourself as a programmer?

The biggest thing I learned is that I can handle a project that feels huge at first by staying patient and thinking step by step.  

At the beginning, planning what feature comes next and learning the exact topics I needed felt overwhelming.  

But I discovered that breaking the work into small, clear pieces and loving the hard work through slow parts turns confusion into a working program.  

I now know I have the patience and strategic thinking to build something real, and that gives me the confidence to start the next versions, next project without fear.
