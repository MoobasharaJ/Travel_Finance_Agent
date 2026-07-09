"""
Pure calculation utilities.

These functions perform only mathematical calculations.
No database operations.
No API calls.
No AI.
"""

from datetime import date


def calculate_total_pre_trip_expenses(expenses: list[float]) -> float:
    """
    Calculate total pre-trip expenses.
    """
    return round(sum(expenses), 2)


def calculate_travel_budget(total_budget: float, pre_trip_expenses: float) -> float:
    """
    Travel Budget = Total Budget - Pre-trip Expenses
    """
    return round(total_budget - pre_trip_expenses, 2)


def calculate_total_expenses(expenses: list[float]) -> float:
    """
    Calculate total trip expenses.
    """
    return round(sum(expenses), 2)


def calculate_remaining_budget(travel_budget: float, total_expenses: float) -> float:
    """
    Remaining budget during the trip.
    """
    return round(travel_budget - total_expenses, 2)


def calculate_trip_duration(start_date: date, end_date: date) -> int:
    """
    Returns total trip duration in days.
    """
    return (end_date - start_date).days + 1


def calculate_days_elapsed(start_date: date, current_date: date) -> int:
    """
    Returns completed trip days.

    Before trip  -> 0
    During trip  -> elapsed days
    After trip   -> total elapsed days
    """

    if current_date < start_date:
        return 0

    return (current_date - start_date).days + 1


def calculate_days_remaining(
    start_date: date,
    end_date: date,
    current_date: date
) -> int:
    """
    Returns remaining travel days.

    Before trip -> Full duration
    During trip -> Remaining days
    After trip -> 0
    """

    if current_date < start_date:
        return calculate_trip_duration(
            start_date,
            end_date
        )

    if current_date > end_date:
        return 0

    return (end_date - current_date).days + 1

def calculate_daily_average(total_expenses: float, days_elapsed: int) -> float:
    """
    Average daily spending.
    """
    if days_elapsed <= 0:
        return 0.0

    return round(total_expenses / days_elapsed, 2)


def calculate_daily_allowance(remaining_budget: float, days_remaining: int) -> float:
    """
    Safe daily spending for the remaining trip.
    """
    if days_remaining <= 0:
        return 0.0

    return round(remaining_budget / days_remaining, 2)


def calculate_trip_progress(
    days_elapsed: int,
    trip_duration: int
) -> float:
    """
    Returns trip completion percentage.
    """

    if trip_duration <= 0:
        return 0.0

    progress = (
        days_elapsed / trip_duration
    ) * 100

    return round(
        min(progress, 100),
        2
    )


def calculate_burn_rate(total_expenses: float, travel_budget: float) -> float:
    """
    Percentage of travel budget already spent.
    """
    if travel_budget <= 0:
        return 0.0

    return round((total_expenses / travel_budget) * 100, 2)


def calculate_category_breakdown(
    expenses: dict
) -> dict:
    """
    Returns actual category totals.

    Example:

    {
        "Food": 3500,
        "Hotel": 15000
    }
    """

    return expenses