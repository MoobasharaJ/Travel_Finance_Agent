"""
Expense Analytics Service

Responsible for:

- Expense analytics
- Budget calculations
- Forecast generation
- Preparing data for AI Router
"""

from services.database_service import (
    get_total_spent,
    get_transaction_count,
    get_category_summary,
    get_highest_spending_category
)

from services.forecasting_service import (
    generate_forecast
)

from utils.calculations import (
    calculate_remaining_budget
)


def get_trip_analytics(
    budget: float,
    current_day: int,
    trip_duration: int
) -> dict:
    """
    Generate complete trip analytics.

    Returns all metrics required by:

    - Dashboard
    - Router
    - AI Agents
    """

    total_spent = get_total_spent()

    transaction_count = get_transaction_count()

    category_summary = get_category_summary()

    highest_category, highest_amount = (
        get_highest_spending_category()
    )

    remaining_budget = (
        calculate_remaining_budget(
            budget,
            total_spent
        )
    )

    forecast = generate_forecast(
        budget=budget,
        total_spent=total_spent,
        current_day=current_day,
        trip_duration=trip_duration
    )

    return {

        "total_spent": total_spent,

        "transaction_count": transaction_count,

        "category_summary": category_summary,

        "highest_spending_category": highest_category,

        "highest_spending_amount": highest_amount,

        "remaining_budget": remaining_budget,

        "forecast": forecast
    }