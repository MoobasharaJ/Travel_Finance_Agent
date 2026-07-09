"""
Travel Service

Business logic for the Travel Finance Agent.

Responsible for:
- Trip creation
- Pre-trip expense management
- Daily expense management
- Dashboard data aggregation

No SQL.
No AI.
No UI.
"""

from datetime import date

from services.database_service import DatabaseService
from services.currency_service import CurrencyService

from utils.calculations import (
    calculate_trip_duration,
    calculate_travel_budget,
    calculate_remaining_budget,
    calculate_days_elapsed,
    calculate_days_remaining,
    calculate_daily_average,
    calculate_daily_allowance,
    calculate_trip_progress,
    calculate_burn_rate,
    calculate_category_breakdown,
)

print("Imported:", calculate_trip_duration)


class TravelService:

    def __init__(self):
        self.db = DatabaseService()
        self.currency_service = CurrencyService()

    # ======================================================
    # Trip Management
    # ======================================================

    def create_trip(
        self,
        destination,
        start_date,
        end_date,
        total_budget,
    ):
        """
        Create a new trip.
        """

        currency = self.currency_service.get_currency(destination)

        duration = calculate_trip_duration(start_date, end_date)

        travel_budget = total_budget

        trip_id = self.db.create_trip(
            destination=destination,
            currency=currency,
            start_date=str(start_date),
            end_date=str(end_date),
            duration=duration,
            total_budget=total_budget,
            travel_budget=travel_budget,
        )

        return trip_id

    # ======================================================
    # Pre-Trip Expenses
    # ======================================================

    def add_pre_trip_expense(self, trip_id, category, amount, notes=""):
        """
        Save a pre-trip expense and
        update travel budget.
        """

        self.db.save_pre_trip_expense(
            trip_id=trip_id, category=category, amount=amount, notes=notes
        )

        total_pre_trip = self.db.get_total_pre_trip_expense(trip_id)

        trip = self.db.get_trip(trip_id)

        travel_budget = calculate_travel_budget(trip["total_budget"], total_pre_trip)

        self.db.update_trip(trip_id, travel_budget)

        return {
            "travel_budget": travel_budget,
            "total_pre_trip_expenses": total_pre_trip,
        }

    # ======================================================
    # Daily Expenses
    # ======================================================

    def add_expense(self, trip_id, expense_date, category, amount, notes=""):
        """
        Save a daily travel expense.
        """

        self.db.save_expense(
            trip_id=trip_id,
            date=str(expense_date),
            category=category,
            amount=amount,
            notes=notes,
        )

        return {"message": "Expense added successfully."}
        # ======================================================

    # Dashboard
    # ======================================================

    def get_dashboard_data(self, trip_id):
        """
        Collect and return complete dashboard data.
        """

        # ==================================================
        # Trip Details
        # ==================================================

        trip = self.db.get_trip(trip_id)

        if trip is None:
            return None

        # ==================================================
        # Expenses
        # ==================================================

        total_expense = self.db.get_total_expense(trip_id)

        total_pre_trip = self.db.get_total_pre_trip_expense(trip_id)

        category_totals = self.db.get_category_totals(trip_id)

    # ==================================================
    # Budget Calculations
    # ==================================================

        remaining_budget = calculate_remaining_budget(trip["travel_budget"], total_expense)

        today = date.today()

        start_date = date.fromisoformat(trip["start_date"])

        end_date = date.fromisoformat(trip["end_date"])

    # ==================================================
    # Trip Status
    # ==================================================

        if today < start_date:

           trip_status = "Not Started"

           days_until_trip = (start_date - today).days

        elif today > end_date:

           trip_status = "Completed"

           days_until_trip = 0

        else:

          trip_status = "In Progress"

          days_until_trip = 0

    # ==================================================
    # Trip Analytics
    # ==================================================

        days_elapsed = calculate_days_elapsed(start_date, today)

        days_remaining = calculate_days_remaining(end_date, today)

        daily_average = calculate_daily_average(total_expense, days_elapsed)

        daily_allowance = calculate_daily_allowance(remaining_budget, days_remaining)

        trip_progress = calculate_trip_progress(days_elapsed, trip["duration"])

        burn_rate = calculate_burn_rate(total_expense, trip["travel_budget"])

        category_breakdown = calculate_category_breakdown(category_totals)
            # ==================================================
    # Top Spending Category
    # ==================================================

        if category_totals:

           top_spending_category = max(
            category_totals,
            key=category_totals.get
        )

        else:

           top_spending_category = None

    # ==================================================
    # Forex
    # ==================================================

        live_rate = self.currency_service.get_live_exchange_rate(
           trip["currency"]
       )

        travel_budget_forex = (
            self.currency_service.convert_currency(
                trip["travel_budget"],
                live_rate["exchange_rate"]
            )
        )

        remaining_budget_forex = (
             self.currency_service.convert_currency(
               remaining_budget,
               live_rate["exchange_rate"]
            )
       )

        daily_allowance_forex = (
            self.currency_service.convert_currency(
              daily_allowance,
               live_rate["exchange_rate"]
            )
        )

    # ==================================================
    # Historical Forex
    # ==================================================

        trend_7 = self.currency_service.analyze_trend(
            self.currency_service.get_historical_rates(
              trip["currency"],
              7
            )
        )

        trend_30 = self.currency_service.analyze_trend(
            self.currency_service.get_historical_rates(
                trip["currency"],
                30
            )
        )
        # ==================================================
    # Dashboard Data
    # ==================================================

        return {

        "trip": trip,

        "analytics": {

            "total_expense": total_expense,

            "remaining_budget": remaining_budget,

            "daily_average": daily_average,

            "daily_allowance": daily_allowance,

            "trip_progress": trip_progress,

            "burn_rate": burn_rate,

            "category_breakdown": category_breakdown,

            # New Fields
            "pre_trip_expenses": total_pre_trip,

            "trip_status": trip_status,

            "days_until_trip": days_until_trip,

            "top_spending_category": top_spending_category,
        },

        "currency_conversion": {

            "travel_budget": travel_budget_forex,

            "remaining_budget": remaining_budget_forex,

            "daily_allowance": daily_allowance_forex,
        },

        "forex": {

            "live_rate": live_rate,

            "7_day": trend_7,

            "30_day": trend_30,
        }
    }