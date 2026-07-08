"""
Utility functions for deterministic calculations.

This module contains reusable calculation
functions used across the Travel Finance Agent.
"""

from datetime import date


def calculate_trip_duration(
    start_date,
    end_date
):
    """
    Calculate total trip duration in days.
    """

    return (
        end_date - start_date
    ).days + 1


def calculate_current_day(
    start_date,
    end_date
):
    """
    Calculate which day of the trip
    the traveler is currently on.
    """

    today = date.today()

    trip_duration = (
        end_date - start_date
    ).days + 1

    if today < start_date:
        return 0

    if today > end_date:
        return trip_duration

    return (
        today - start_date
    ).days + 1


def calculate_trip_progress(
    current_day,
    trip_duration
):
    """
    Calculate trip completion percentage.
    """

    if trip_duration <= 0:
        return 0

    return round(
        (current_day / trip_duration) * 100,
        2
    )


def calculate_budget_used(
    total_spent,
    budget
):
    """
    Calculate percentage of budget used.
    """

    if budget <= 0:
        return 0

    return round(
        (total_spent / budget) * 100,
        2
    )


def calculate_remaining_budget(
    budget,
    total_spent
):
    """
    Calculate remaining budget.
    """

    return budget - total_spent


def calculate_average_daily_spend(
    total_spent,
    current_day
):
    """
    Calculate average daily spending.
    """

    if current_day <= 0:
        return 0

    return round(
        total_spent / current_day,
        2
    )


def calculate_projected_spend(
    average_daily_spend,
    trip_duration
):
    """
    Estimate total spending by
    the end of the trip.
    """

    return round(
        average_daily_spend * trip_duration,
        2
    )


def calculate_projected_difference(
    budget,
    projected_spend
):
    """
    Positive value:
        Budget remaining

    Negative value:
        Overspending
    """

    return round(
        budget - projected_spend,
        2
    )