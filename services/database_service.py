"""
SQLite Database Service

Handles:
- Database creation
- Expense insertion
- Expense retrieval
- Category summaries
"""

import sqlite3
import pandas as pd

from utils.constants import DATABASE_NAME


def get_connection():
    """
    Create database connection.
    """

    return sqlite3.connect(DATABASE_NAME)


def create_database():
    """
    Create expenses table if it doesn't exist.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def add_expense(
    category,
    amount,
    currency,
    description=""
):
    """
    Insert expense into database.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses
        (
            category,
            amount,
            currency,
            description
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            category,
            amount,
            currency,
            description
        )
    )

    conn.commit()
    conn.close()


def get_all_expenses():
    """
    Return all expenses.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM expenses
    ORDER BY created_at DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def get_total_spent():
    """
    Calculate total spent.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(
            SUM(amount),
            0
        )
        FROM expenses
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_transaction_count():
    """
    Return total transactions.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM expenses
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_category_summary():
    """
    Return category-wise spending.
    """

    conn = get_connection()

    query = """
    SELECT
        category AS Category,
        SUM(amount) AS Amount
    FROM expenses
    GROUP BY category
    ORDER BY Amount DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def get_highest_spending_category():
    """
    Return highest spending category.
    """

    summary = get_category_summary()

    if summary.empty:
        return None, 0

    category = summary.iloc[0]["Category"]
    amount = summary.iloc[0]["Amount"]

    return category, amount