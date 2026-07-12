"""
Travel Service

Business logic for the Travel Finance Agent.

Responsible for:
- Trip creation
- Expense management
- Dashboard data aggregation

No SQL.
No AI.
No UI.
"""

from datetime import date
from utils.constants import PRE_TRIP, TRAVEL
from services.database_service import DatabaseService
from services.currency_service import CurrencyService

from services.google_places_service import GooglePlacesService
from services.llm_service import LLMService

from prompts.finance_prompt import (
    build_nearby_recommendation_prompt,
)

from utils.calculations import (
    calculate_travel_budget,
    calculate_remaining_budget,
    calculate_trip_duration,
    calculate_days_elapsed,
    calculate_days_remaining,
    calculate_daily_allowance,
)

class TravelService:

    def __init__(self):

        self.db = DatabaseService()

        self.currency_service = CurrencyService()

        self.google_places_service = GooglePlacesService()

        self.llm_service = LLMService()

    # ======================================================
    # Trip Management
    # ======================================================

    def create_trip(
       self,
       home_country,
       destination_country,
       start_date,
       end_date,
      total_budget,
    ):
     """
    Create a new trip.
    """

     home_currency = self.currency_service.get_currency(home_country)

     destination_currency = self.currency_service.get_currency(
        destination_country
     )

     trip_id = self.db.create_trip(
        home_country=home_country,
        home_currency=home_currency,
        destination_country=destination_country,
        destination_currency=destination_currency,
        start_date=str(start_date),
        end_date=str(end_date),
        total_budget=total_budget,
     )

     return trip_id

    # ======================================================
    # Daily Expenses
    # ======================================================

    def add_expense(
      self,
      trip_id,
      expense_type,
      expense_date,
      category,
      amount,
      currency,
      notes="",
    ):
     """
     Save an expense.
     """

     self.db.save_expense(
        trip_id=trip_id,
        expense_type=expense_type,
        date=str(expense_date),
        category=category,
        amount=amount,
        currency=currency,
        notes=notes,
    )

     return {
        "message": "Expense added successfully."
    }
        # ======================================================
    # GET TRIP SUMMARY
    # ======================================================
    def get_trip_summary(self, trip_id):

        trip = self.db.get_trip(trip_id)
        if trip is None:
          return None
        
            # ==================================================
        # Expenses
        # ==================================================

        #total_expense = self.db.get_total_expense(trip_id)

        #total_pre_trip = self.db.get_total_pre_trip_expense(trip_id)

        #category_totals = self.db.get_category_totals(trip_id)
        expenses = self.db.get_expenses(trip_id)

        total_expense = 0.0

        total_pre_trip = 0.0

        category_totals = {}

        for expense in expenses:

            amount = expense["amount"]
 
            currency = expense["currency"]

            expense_type = expense["expense_type"]

            category = expense["category"]

            if currency != trip["home_currency"]:

                amount = self.currency_service.convert_between_currencies(
                    amount=amount,
                    from_currency=currency,
                    to_currency=trip["home_currency"],
                )

            if expense_type == PRE_TRIP:

                total_pre_trip += amount

            elif expense_type == TRAVEL:

                total_expense += amount 

            if expense_type == TRAVEL:

               if category not in category_totals:

                category_totals[category] = 0.0

               category_totals[category] += amount  


        total_expense = round(total_expense, 2)

        total_pre_trip = round(total_pre_trip, 2)       
    # ==================================================
    # Budget Calculations
    # ==================================================

        travel_budget = calculate_travel_budget(
           trip["total_budget"],
           total_pre_trip
            )

        remaining_budget = calculate_remaining_budget(
         travel_budget,
         total_expense
         )
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

        days_remaining = calculate_days_remaining(start_date, end_date, today)

        daily_allowance = calculate_daily_allowance(remaining_budget, days_remaining)

        trip_duration = calculate_trip_duration(start_date, end_date)
        
        category_breakdown = category_totals
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


        return {

                "trip": trip,

                   "analytics": {

                     "total_expense": total_expense,

                     "total_budget": trip["total_budget"],

                     "travel_budget": travel_budget,

                     "remaining_budget": remaining_budget,

                     "daily_allowance": daily_allowance,

                     "pre_trip_expenses": total_pre_trip,

                     "trip_duration": trip_duration,

                     "days_elapsed": days_elapsed,

                     "days_remaining": days_remaining,

                     "trip_status": trip_status,

                     "days_until_trip": days_until_trip,

                     "top_spending_category": top_spending_category,
                     
                     "category_breakdown": category_breakdown, 
                   }

             }


        # ======================================================

    # Dashboard
    # ======================================================

    def get_dashboard_data(self, trip_id):
        """
        Collect and return complete dashboard data.
        """
        #print("===== GET DASHBOARD DATA CALLED =====")
        summary = self.get_trip_summary(trip_id)

        if summary is None:
           return None

        trip = summary["trip"]

        analytics = summary["analytics"]

        total_budget = analytics["total_budget"]

        travel_budget = analytics["travel_budget"]

        total_pre_trip = analytics["pre_trip_expenses"]

        total_expense = analytics["total_expense"]

        remaining_budget = analytics["remaining_budget"]

        daily_allowance = analytics["daily_allowance"]
    # ==================================================
    # Forex
    # ==================================================

        live_rate = self.currency_service.get_live_exchange_rate(
         trip["home_currency"],
          trip["destination_currency"]
         )

        travel_budget_forex = (
            self.currency_service.convert_currency(
                travel_budget,
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
        pre_trip_forex = (
            self.currency_service.convert_currency(
              total_pre_trip,
              live_rate["exchange_rate"]
            )
        )

        total_budget_forex = (
            self.currency_service.convert_currency(
            total_budget,
              live_rate["exchange_rate"]
            )
       )
        spent_forex = self.currency_service.convert_currency(
             total_expense,
             live_rate["exchange_rate"]
   )

    # ==================================================
    # Historical Forex
    # ==================================================

        trend_7 = self.currency_service.analyze_trend(
            self.currency_service.get_historical_rates(
            trip["home_currency"],
            trip["destination_currency"],
             7
            )
        )

        trend_30 = self.currency_service.analyze_trend(
            self.currency_service.get_historical_rates(
            trip["home_currency"],
            trip["destination_currency"],
            30
            )
       )
        # ==================================================
    # Dashboard Data
    # ==================================================
        
        return {

    "trip": trip,

    "analytics": analytics,

    "currency_conversion": {

        "total_budget": total_budget_forex,

        "travel_budget": travel_budget_forex,

        "pre_trip_expenses": pre_trip_forex,

        "remaining_budget": remaining_budget_forex,

        "daily_allowance": daily_allowance_forex,

        "spent": spent_forex,
    },

    "forex": {

        "live_rate": live_rate,

        "7_day": trend_7,

        "30_day": trend_30,
    }
}
    
        # ======================================================
    # Nearby Recommendations
    # ======================================================

    def get_nearby_recommendations(
        self,
        trip_id,
        city,
        category,
    ):
        """
        Get nearby places from Google Places and let Gemini
        recommend the best options based on travel budget.
        """

        dashboard = self.get_dashboard_data(trip_id)

        # ----------------------------------------------
        # Google Places Search
        # ----------------------------------------------

        if category == "restaurant":

            places = self.google_places_service.search_budget_restaurants(
                city
            )

        elif category == "atm":

            places = self.google_places_service.search_atms(
                city
            )

        elif category == "currency_exchange":

            places = self.google_places_service.search_currency_exchange(
                city
            )

        elif category == "convenience_store":

            places = self.google_places_service.search_convenience_stores(
                city
            )

        else:

            return "Invalid category."

        if not places:

            return (
                f"No nearby {category.replace('_', ' ')} "
                f"were found."
            )

        # ----------------------------------------------
        # Build Prompt
        # ----------------------------------------------

        prompt = build_nearby_recommendation_prompt(
            dashboard=dashboard,
            places=places,
            category=category.replace("_", " "),
        )

        # ----------------------------------------------
        # Gemini Recommendation
        # ----------------------------------------------

        return self.llm_service.generate_response(
            prompt
        )