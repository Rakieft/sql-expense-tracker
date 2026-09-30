# Overview

As a software developer, I wanted to build practical experience working with relational databases, since almost every real-world application needs to store and query structured data. This project is a Personal Expense Tracker that uses a SQL database (SQLite) to store expenses and categories, and lets the user manage that data from a command-line menu.

The program lets the user insert new expenses, update or delete existing ones, list all expenses (joined with their category name), see a summary of total spending per category, and filter expenses within a specific date range. Run it with `python expense_tracker.py` and follow the on-screen menu.

My purpose in writing this software was to practice designing a relational schema with a foreign key relationship, and to practice building and executing real SQL statements from Python instead of only using an ORM.

[Software Demo Video](http://youtube.link.goes.here)

# Relational Database

I used SQLite (via Python's built-in `sqlite3` library), which stores the entire database in a single local file (`expenses.db`).

The database has two related tables:

- **categories** — `id` (primary key), `name` (unique category name, e.g. "Groceries")
- **expenses** — `id` (primary key), `category_id` (foreign key referencing `categories.id`), `amount`, `description`, `expense_date`

Every expense belongs to exactly one category, so listing expenses or summarizing spending requires a `JOIN` between the two tables.

# Development Environment

I used Visual Studio Code as my code editor and Git for version control, with the code hosted on GitHub.

I wrote the program in Python, using the built-in `sqlite3` library to create the database, build SQL statements (`INSERT`, `UPDATE`, `DELETE`, `SELECT` with `JOIN`, aggregate functions, and `BETWEEN` for date filtering), execute them, and use the returned results.

# Useful Websites

- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite documentation](https://www.sqlite.org/docs.html)
- [W3Schools SQL Joins](https://www.w3schools.com/sql/sql_join.asp)

# Future Work

- Add a graphical interface instead of a command-line menu
- Add a "budget" table so users can set a spending limit per category
- Export expense reports to a CSV file
