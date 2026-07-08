"""
Currency Service

Handles:
- Destination currency lookup
- Live exchange rates
- Currency conversion
- Exchange rate insights
"""

from typing import Dict, Optional

import requests

from utils.constants import (
    DESTINATION_TO_CURRENCY,
    EXCHANGE_RATE_BASE_URL
)


def get_currency_for_destination(
    destination: str
) -> Optional[str]:
    """
    Return currency code for the selected destination.

    Example:
        Japan -> JPY
        France -> EUR

    Returns:
        str | None
    """

    return DESTINATION_TO_CURRENCY.get(
        destination
    )


def get_exchange_rates(
    base_currency: str = "INR"
) -> Dict:
    """
    Fetch live exchange rates for a base currency.

    Returns:
        dict of exchange rates

    Example:
        {
            "USD": 0.012,
            "JPY": 1.73,
            ...
        }
    """

    try:

        url = (
            f"{EXCHANGE_RATE_BASE_URL}/"
            f"{base_currency}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("result") == "success":

            return data.get(
                "rates",
                {}
            )

        return {}

    except Exception as e:

        print(
            f"Exchange rate fetch error: {e}"
        )

        return {}


def get_live_exchange_rate(
    base_currency: str,
    target_currency: str
) -> Optional[float]:
    """
    Get live exchange rate between two currencies.

    Example:
        INR -> JPY
        returns 1.73
    """

    rates = get_exchange_rates(
        base_currency
    )

    return rates.get(
        target_currency
    )


def convert_currency(
    amount: float,
    base_currency: str,
    target_currency: str
) -> Optional[float]:
    """
    Convert amount from one currency
    to another.

    Example:
        1000 INR -> JPY
    """

    rate = get_live_exchange_rate(
        base_currency,
        target_currency
    )

    if rate is None:

        return None

    return round(
        amount * rate,
        2
    )


def convert_inr_to_destination(
    amount_inr: float,
    destination_currency: str
) -> Optional[float]:
    """
    Convert INR to destination currency.
    """

    return convert_currency(
        amount_inr,
        "INR",
        destination_currency
    )


def convert_destination_to_inr(
    amount: float,
    source_currency: str
) -> Optional[float]:
    """
    Convert destination currency to INR.
    """

    return convert_currency(
        amount,
        source_currency,
        "INR"
    )


def generate_exchange_rate_insight(
    rate: Optional[float],
    destination_currency: str
) -> str:
    """
    Generate exchange-rate insight
    for dashboard display.
    """

    if rate is None:

        return (
            "Unable to fetch live "
            "exchange rate data."
        )

    return (
        f"1 INR = {rate:.4f} "
        f"{destination_currency}"
    )