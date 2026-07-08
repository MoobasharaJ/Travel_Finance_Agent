"""
SQLite Database Service

Responsible for:
- Creating database tables
- CRUD operations for trips
- CRUD operations for pre-trip expenses
- CRUD operations for daily expenses

No calculations.
No AI.
No business logic.
"""

import sqlite3
from datetime import datetime

from utils.constants import DATABASE_PATH


class DatabaseService:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.create_tables()

    # ==========================================================
    # Create Tables
    # ==========================================================

    def create_tables(self):
        """Create all required tables if they don't exist."""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                currency TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                duration INTEGER NOT NULL,
                total_budget REAL NOT NULL,
                travel_budget REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pre_trip_expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            )
        """)

        self.conn.commit()

    # ==========================================================
    # Trip Methods
    # ==========================================================

    def create_trip(
        self,
        destination,
        currency,
        start_date,
        end_date,
        duration,
        total_budget,
        travel_budget,
    ):
        """Create a new trip."""

        self.cursor.execute("""
            INSERT INTO trips (
                destination,
                currency,
                start_date,
                end_date,
                duration,
                total_budget,
                travel_budget,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            destination,
            currency,
            start_date,
            end_date,
            duration,
            total_budget,
            travel_budget,
            datetime.now().isoformat()
        ))

        self.conn.commit()

        return self.cursor.lastrowid

    def get_trip(self, trip_id):
        """Return a single trip."""

        self.cursor.execute(
            "SELECT * FROM trips WHERE trip_id = ?",
            (trip_id,)
        )

        row = self.cursor.fetchone()

        return dict(row) if row else None

    def update_trip(self, trip_id, travel_budget):
        """Update travel budget."""

        self.cursor.execute("""
            UPDATE trips
            SET travel_budget = ?
            WHERE trip_id = ?
        """, (travel_budget, trip_id))

        self.conn.commit()

    # ==========================================================
    # Pre-Trip Expense Methods
    # ==========================================================

    def save_pre_trip_expense(
        self,
        trip_id,
        category,
        amount,
        notes=""
    ):
        """Save a pre-trip expense."""

        self.cursor.execute("""
            INSERT INTO pre_trip_expenses (
                trip_id,
                category,
                amount,
                notes
            )
            VALUES (?, ?, ?, ?)
        """, (
            trip_id,
            category,
            amount,
            notes
        ))

        self.conn.commit()

    def get_pre_trip_expenses(self, trip_id):
        """Return all pre-trip expenses."""

        self.cursor.execute("""
            SELECT *
            FROM pre_trip_expenses
            WHERE trip_id = ?
        """, (trip_id,))

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    # ==========================================================
    # Daily Expense Methods
    # ==========================================================

    def save_expense(
        self,
        trip_id,
        date,
        category,
        amount,
        notes=""
    ):
        """Save a daily expense."""

        self.cursor.execute("""
            INSERT INTO expenses (
                trip_id,
                date,
                category,
                amount,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            trip_id,
            date,
            category,
            amount,
            notes
        ))

        self.conn.commit()

    def get_expenses(self, trip_id):
        """Return all expenses for a trip."""

        self.cursor.execute("""
            SELECT *
            FROM expenses
            WHERE trip_id = ?
            ORDER BY date ASC
        """, (trip_id,))

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    def delete_expense(self, expense_id):
        """Delete an expense."""

        self.cursor.execute("""
            DELETE FROM expenses
            WHERE expense_id = ?
        """, (expense_id,))

        self.conn.commit()

    def get_total_pre_trip_expense(self, trip_id):
       """
        Return total pre-trip expenses.
       """

       self.cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM pre_trip_expenses
        WHERE trip_id = ?
        """, (trip_id,))

       row = self.cursor.fetchone()

       return row["total"]


    def get_total_expense(self, trip_id):
        """
        Return total trip expenses.
        """

        self.cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE trip_id = ?
        """, (trip_id,))

        row = self.cursor.fetchone()

        return row["total"]
    
    def get_category_totals(self, trip_id):
        """
        Return category-wise expense totals.
        """

        self.cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total
        FROM expenses
        WHERE trip_id = ?
        GROUP BY category
        """, (trip_id,))

        rows = self.cursor.fetchall()

        return {
        row["category"]: row["total"]
        for row in rows
        }
    # ==========================================================
    # Close Connection
    # ==========================================================

    def close(self):
        """Close the database connection."""

        self.conn.close()