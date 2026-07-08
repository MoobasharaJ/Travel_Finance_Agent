"""
Currency Service

Responsible for:
- Destination currency lookup
- Live exchange rates
- Historical exchange rates
- Currency conversion
- Forex trend analysis

No database.
No AI.
No business logic.
"""

from datetime import datetime, timedelta

import requests

from utils.constants import (
    SUPPORTED_DESTINATIONS,
    HOME_CURRENCY,
    LIVE_FOREX_API_URL,
    HISTORICAL_FOREX_API_URL,
)


class CurrencyService:

    # ======================================================
    # Destination
    # ======================================================

    def get_currency(self, destination):
        """Return currency code for a destination."""
        return SUPPORTED_DESTINATIONS.get(destination)

    # ======================================================
    # Live Exchange Rate
    # ======================================================

    def get_live_exchange_rate(self, currency):
        """
        Returns INR -> Destination exchange rate.
        """

        response = requests.get(
            f"{LIVE_FOREX_API_URL}/{HOME_CURRENCY}"
        )

        response.raise_for_status()

        data = response.json()

        return {
            "base_currency": HOME_CURRENCY,
            "target_currency": currency,
            "exchange_rate": data["rates"][currency]
        }

    # ======================================================
    # Currency Conversion
    # ======================================================

    def convert_currency(self, amount, exchange_rate):
        """
        Convert INR into destination currency.
        """
        return round(amount * exchange_rate, 2)
    
    def convert_to_inr(amount, exchange_rate):

       return round(amount / exchange_rate, 2)

    # ======================================================
    # Historical Rates
    # ======================================================

    def get_historical_rates(self, currency, days=30):
        """
        Returns historical INR -> destination currency rates.
        """

        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=days)

        url = (
            f"{HISTORICAL_FOREX_API_URL}/"
            f"{start_date}..{end_date}"
            f"?from={HOME_CURRENCY}"
            f"&to={currency}"
        )

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        rates = []

        for date, value in data["rates"].items():
            rates.append({
                "date": date,
                "rate": value[currency]
            })

        return rates

    # ======================================================
    # Trend Analysis
    # ======================================================

    def analyze_trend(self, rates):
        """
        Analyze historical forex trend.
        """

        if not rates:
            return None

        values = [item["rate"] for item in rates]

        current_rate = values[-1]

        first_rate = values[0]

        moving_average = round(sum(values) / len(values), 4)

        percentage_change = round(
            ((current_rate - first_rate) / first_rate) * 100,
            2
        )

        if percentage_change > 0.5:
            trend = "Up"

        elif percentage_change < -0.5:
            trend = "Down"

        else:
            trend = "Stable"

        return {
            "current_rate": current_rate,
            "moving_average": moving_average,
            "percentage_change": percentage_change,
            "trend": trend
        }