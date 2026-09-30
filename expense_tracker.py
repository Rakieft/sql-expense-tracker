import sqlite3
from datetime import date

DB_PATH = "expenses.db"


def get_connection():
    """Open a connection to the SQLite database file."""
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    """Create the categories and expenses tables if they don't exist yet.

    expenses.category_id is a foreign key into categories.id, so the two
    tables can be joined together later.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)
    conn.commit()


def seed_sample_data(conn):
    """Insert a few sample categories and expenses if the database is empty.

    This gives the program something to show immediately during a demo.
    """
    existing = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    if existing > 0:
        return

    categories = ["Groceries", "Transportation", "Entertainment", "Utilities"]
    for name in categories:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))

    sample_expenses = [
        ("Groceries", 54.32, "Weekly grocery run", "2026-09-02"),
        ("Groceries", 21.10, "Snacks", "2026-09-15"),
        ("Transportation", 40.00, "Gas", "2026-09-05"),
        ("Transportation", 15.50, "Bus pass top-up", "2026-09-20"),
        ("Entertainment", 12.99, "Streaming subscription", "2026-09-10"),
        ("Utilities", 85.00, "Electric bill", "2026-09-01"),
    ]
    for category_name, amount, description, expense_date in sample_expenses:
        insert_expense(conn, category_name, amount, description, expense_date)
    conn.commit()


def get_or_create_category(conn, category_name):
    """Return the id of a category, creating it first if it doesn't exist."""
    row = conn.execute("SELECT id FROM categories WHERE name = ?", (category_name,)).fetchone()
    if row:
        return row[0]
    cursor = conn.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()
    return cursor.lastrowid


def insert_expense(conn, category_name, amount, description, expense_date):
    """Insert a new expense under the given category name."""
    category_id = get_or_create_category(conn, category_name)
    conn.execute(
        "INSERT INTO expenses (category_id, amount, description, expense_date) VALUES (?, ?, ?, ?)",
        (category_id, amount, description, expense_date),
    )
    conn.commit()


def update_expense_amount(conn, expense_id, new_amount):
    """Modify the amount of an existing expense by its id."""
    conn.execute("UPDATE expenses SET amount = ? WHERE id = ?", (new_amount, expense_id))
    conn.commit()


def delete_expense(conn, expense_id):
    """Delete an expense by its id."""
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()


def list_all_expenses(conn):
    """Retrieve every expense, joined with its category name, newest first."""
    query = """
        SELECT expenses.id, categories.name, expenses.amount, expenses.description, expenses.expense_date
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        ORDER BY expenses.expense_date DESC
    """
    return conn.execute(query).fetchall()


def summarize_spending_by_category(conn):
    """Use a join plus aggregate functions to total spending per category."""
    query = """
        SELECT categories.name, SUM(expenses.amount) AS total_spent, COUNT(expenses.id) AS num_expenses
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        GROUP BY categories.name
        ORDER BY total_spent DESC
    """
    return conn.execute(query).fetchall()


def filter_expenses_by_date_range(conn, start_date, end_date):
    """Retrieve expenses whose date falls within the given range (inclusive)."""
    query = """
        SELECT expenses.id, categories.name, expenses.amount, expenses.description, expenses.expense_date
        FROM expenses
        JOIN categories ON expenses.category_id = categories.id
        WHERE expenses.expense_date BETWEEN ? AND ?
        ORDER BY expenses.expense_date
    """
    return conn.execute(query, (start_date, end_date)).fetchall()


def print_expenses(rows):
    """Print a list of (id, category, amount, description, date) rows."""
    if not rows:
        print("No expenses found.")
        return
    for expense_id, category, amount, description, expense_date in rows:
        print(f"  #{expense_id} | {expense_date} | {category:15} | ${amount:8.2f} | {description}")


def print_summary(rows):
    """Print a list of (category, total_spent, num_expenses) rows."""
    for category, total_spent, num_expenses in rows:
        print(f"  {category:15} | ${total_spent:8.2f} total | {num_expenses} expense(s)")


def print_menu():
    print("\n--- Personal Expense Tracker ---")
    print("1. List all expenses")
    print("2. Add an expense")
    print("3. Update an expense's amount")
    print("4. Delete an expense")
    print("5. Show spending summary by category")
    print("6. Filter expenses by date range")
    print("7. Exit")


def main():
    conn = get_connection()
    create_tables(conn)
    seed_sample_data(conn)

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            print_expenses(list_all_expenses(conn))
        elif choice == "2":
            category_name = input("Category: ").strip()
            amount = float(input("Amount: ").strip())
            description = input("Description: ").strip()
            expense_date = input("Date (YYYY-MM-DD), leave blank for today: ").strip() or str(date.today())
            insert_expense(conn, category_name, amount, description, expense_date)
            print("Expense added.")
        elif choice == "3":
            expense_id = int(input("Expense id to update: ").strip())
            new_amount = float(input("New amount: ").strip())
            update_expense_amount(conn, expense_id, new_amount)
            print("Expense updated.")
        elif choice == "4":
            expense_id = int(input("Expense id to delete: ").strip())
            delete_expense(conn, expense_id)
            print("Expense deleted.")
        elif choice == "5":
            print_summary(summarize_spending_by_category(conn))
        elif choice == "6":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()
            print_expenses(filter_expenses_by_date_range(conn, start_date, end_date))
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-7.")

    conn.close()


if __name__ == "__main__":
    main()
