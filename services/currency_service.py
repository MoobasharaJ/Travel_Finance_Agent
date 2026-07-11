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
    SUPPORTED_COUNTRIES,
    LIVE_FOREX_API_URL,
    HISTORICAL_FOREX_API_URL,
)


class CurrencyService:
      
    def __init__(self):
        # Cache for exchange rates
        self.exchange_rate_cache = {}
    # ======================================================
    # # Country & Currency
    # ======================================================

    def get_currency(self, country):
        """
        Return currency code for a country.
       """
        return SUPPORTED_COUNTRIES[country]["currency"]
    # ======================================================
    # Live Exchange Rate
    # ======================================================

    def get_live_exchange_rate(
        self,
        base_currency,
        target_currency,
):
       """
       Return live exchange rate between two currencies.
    """
       cache_key = f"{base_currency}_{target_currency}"

       if cache_key in self.exchange_rate_cache:
         return self.exchange_rate_cache[cache_key]
       

       response = requests.get(
        f"{LIVE_FOREX_API_URL}/{base_currency}"
       )

       response.raise_for_status()

       data = response.json()

       result = {
        "base_currency": base_currency,
        "target_currency": target_currency,
         "exchange_rate": data["rates"][target_currency],
         }

       self.exchange_rate_cache[cache_key] = result

       return result

    # ======================================================
    # Currency Conversion
    # ======================================================

    def convert_currency(self, amount, exchange_rate):
       """
       Convert an amount using the provided exchange rate.
    """
       return round(amount * exchange_rate, 2)
    
        # ======================================================
    # Convert Between Two Currencies
    # ======================================================

    def convert_between_currencies(
        self,
        amount,
        from_currency,
        to_currency,
    ):
        """
        Convert an amount from one currency to another.
        """

        # No conversion required
        if from_currency == to_currency:
            return round(amount, 2)

        # Fetch live exchange rate
        live_rate = self.get_live_exchange_rate(
            from_currency,
            to_currency,
        )

        return self.convert_currency(
            amount,
            live_rate["exchange_rate"],
        )
    
    # ======================================================
    # Historical Rates
    # ======================================================

    def get_historical_rates(self, base_currency,  target_currency, days=30,):
    
        """
        Returns historical exchange rates between two currencies.
      """

        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=days)

        url = (
            f"{HISTORICAL_FOREX_API_URL}/"
            f"{start_date}..{end_date}"
            f"?from={base_currency}"
            f"&to={target_currency}"
        )

        response = requests.get(url)

        if response.status_code != 200:
          return []

        data = response.json()

        rates = []

        for date, value in data["rates"].items():
            rates.append({
                "date": date,
                "rate": value[target_currency]
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
         return {
          "current_rate": None,
          "moving_average": None,
          "percentage_change": 0,
          "trend": "Unavailable"
        }

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