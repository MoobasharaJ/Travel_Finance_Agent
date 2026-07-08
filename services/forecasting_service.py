"""
Forecasting Service

Responsible for:

- Budget forecasting
- Spending projections
- Budget health analysis
- Travel finance status generation
"""

from utils.calculations import (
    calculate_budget_used,
    calculate_trip_progress,
    calculate_average_daily_spend,
    calculate_projected_spend,
    calculate_projected_difference
)

from utils.constants import (
    STATUS_ON_TRACK,
    STATUS_WARNING,
    STATUS_OVERSPENDING,
    WARNING_THRESHOLD_PERCENT,
    CRITICAL_THRESHOLD_PERCENT
)


def generate_budget_status(
    budget_used_percent
):
    """
    Determine budget health status.
    """

    if budget_used_percent >= CRITICAL_THRESHOLD_PERCENT:
        return STATUS_OVERSPENDING

    if budget_used_percent >= WARNING_THRESHOLD_PERCENT:
        return STATUS_WARNING

    return STATUS_ON_TRACK


def generate_forecast(
    budget,
    total_spent,
    current_day,
    trip_duration
):
    """
    Generate complete travel budget forecast.

    Returns a dictionary containing
    all forecasting metrics.
    """

    budget_used_percent = (
        calculate_budget_used(
            total_spent,
            budget
        )
    )

    trip_progress_percent = (
        calculate_trip_progress(
            current_day,
            trip_duration
        )
    )

    average_daily_spend = (
        calculate_average_daily_spend(
            total_spent,
            current_day
        )
    )

    projected_total_spend = (
        calculate_projected_spend(
            average_daily_spend,
            trip_duration
        )
    )

    projected_difference = (
        calculate_projected_difference(
            budget,
            projected_total_spend
        )
    )

    status = generate_budget_status(
        budget_used_percent
    )

    return {
        "budget_used_percent":
            budget_used_percent,

        "trip_progress_percent":
            trip_progress_percent,

        "average_daily_spend":
            average_daily_spend,

        "projected_total_spend":
            projected_total_spend,

        "projected_difference":
            projected_difference,

        "status":
            status
    }