"""
SQLite Database Service

Responsible for:
- Creating database tables
- CRUD operations for trips
- CRUD operations for expenses

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
    def create_tables(self):
        """Create all required tables."""

    # ======================================================
    # Trips
    # ======================================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (

            trip_id INTEGER PRIMARY KEY AUTOINCREMENT,

            home_country TEXT NOT NULL,

            home_currency TEXT NOT NULL,

            destination_country TEXT NOT NULL,

            destination_currency TEXT NOT NULL,

            start_date TEXT NOT NULL,

            end_date TEXT NOT NULL,

            total_budget REAL NOT NULL,

            created_at TEXT NOT NULL
        )
    """)

    # ======================================================
    # Expenses
    # ======================================================

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (

            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,

            trip_id INTEGER NOT NULL,

            expense_type TEXT NOT NULL,

            date TEXT NOT NULL,

            category TEXT NOT NULL,

            amount REAL NOT NULL,

            currency TEXT NOT NULL,

            notes TEXT,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL,

            FOREIGN KEY (trip_id)
                REFERENCES trips(trip_id)
                ON DELETE CASCADE
        )
    """)

        self.conn.commit()

    # ==========================================================
    # Trip Methods
    # ==========================================================

    def create_trip(
    self,
    home_country,
    home_currency,
    destination_country,
    destination_currency,
    start_date,
    end_date,
    total_budget,
):
      """Create a new trip."""

      self.cursor.execute("""
        INSERT INTO trips (

            home_country,
            home_currency,
            destination_country,
            destination_currency,
            start_date,
            end_date,
            total_budget,
            created_at

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """, (

          home_country,
          home_currency,
          destination_country,
          destination_currency,
          start_date,
          end_date,
          total_budget,
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

    def update_trip(
    self,
    trip_id,
    start_date,
    end_date,
    total_budget,
):
      """Update editable trip details."""

      self.cursor.execute("""
        UPDATE trips
        SET

            start_date = ?,
            end_date = ?,
            total_budget = ?

        WHERE trip_id = ?
      """, (

          start_date,
          end_date,
          total_budget,
          trip_id

        ))

      self.conn.commit()

    def delete_trip(self, trip_id):
      """Delete a trip."""

      self.cursor.execute(
        "DELETE FROM trips WHERE trip_id = ?",
        (trip_id,)
      )

      self.conn.commit()
    

    # ==========================================================
    # Daily Expense Methods
    # ==========================================================

    def save_expense(
        self,
        trip_id,
        expense_type,
        date,
        category,
        amount,
        currency,
        notes="",
        ):
        """Save an expense."""

        timestamp = datetime.now().isoformat()

        self.cursor.execute("""
        INSERT INTO expenses (

            trip_id,
            expense_type,
            date,
            category,
            amount,
            currency,
            notes,
            created_at,
            updated_at

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

        trip_id,
        expense_type,
        date,
        category,
        amount,
        currency,
        notes,
        timestamp,
        timestamp

        ))

        self.conn.commit()

    def get_expenses(self, trip_id):
      """Return all expenses."""

      self.cursor.execute("""
          SELECT *
          FROM expenses
          WHERE trip_id = ?
          ORDER BY created_at DESC
        """, (trip_id,))

      rows = self.cursor.fetchall()

      return [dict(row) for row in rows]
    
    def update_expense(
        self,
        expense_id,
        expense_type,
        date,
        category,
        amount,
        currency,
        notes,
        ):
      """Update an expense."""

      self.cursor.execute("""
         UPDATE expenses
          SET

            expense_type = ?,
            date = ?,
            category = ?,
            amount = ?,
            currency = ?,
            notes = ?,
            updated_at = ?

          WHERE expense_id = ?
        """, (

        expense_type,
        date,
        category,
        amount,
        currency,
        notes,
        datetime.now().isoformat(),
        expense_id

       ))

      self.conn.commit()

    def delete_expense(self, expense_id):
        """Delete an expense."""

        self.cursor.execute("""
            DELETE FROM expenses
            WHERE expense_id = ?
        """, (expense_id,))

        self.conn.commit()

    # ==========================================================
# Analytics Queries
# ==========================================================

    def get_total_pre_trip_expense(self, trip_id):
      """
      Return total pre-trip expenses.
      """

      self.cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE trip_id = ?
        AND expense_type = 'PRE_TRIP'
       """, (trip_id,))

      row = self.cursor.fetchone()

      return row["total"]


    def get_total_expense(self, trip_id):
     """
     Return total travel expenses.
     """

     self.cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE trip_id = ?
        AND expense_type = 'TRAVEL'
     """, (trip_id,))

     row = self.cursor.fetchone()

     return row["total"]


    def get_category_totals(self, trip_id):
      """
      Return category-wise totals for travel expenses.
    """

      self.cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total
        FROM expenses
        WHERE trip_id = ?
        AND expense_type = 'TRAVEL'
        GROUP BY category
       """, (trip_id,))

      rows = self.cursor.fetchall()

      return {
        row["category"]: row["total"]
        for row in rows
      }


    def get_today_spending(self, trip_id):
     """
    Return today's total travel spending.
    """

     today = datetime.now().date().isoformat()

     self.cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE trip_id = ?
        AND expense_type = 'TRAVEL'
        AND date = ?
    """, (trip_id, today))

     row = self.cursor.fetchone()

     return row["total"]


    def get_recent_transactions(self, trip_id):
     """
    Return the 3 most recent travel transactions.
    """

     self.cursor.execute("""
        SELECT *
        FROM expenses
        WHERE trip_id = ?
        AND expense_type = 'TRAVEL'
        ORDER BY date DESC, expense_id DESC
        LIMIT 3
     """, (trip_id,))

     rows = self.cursor.fetchall()

     return [dict(row) for row in rows]
    # ==========================================================
    # Close Connection
    # ==========================================================

    def close(self):
        """Close the database connection."""

        self.conn.close()