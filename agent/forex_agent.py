"""
Forex Agent

Responsible for:

- Currency analysis
- Exchange rate insights
- Travel forex recommendations
"""

from prompts.finance_prompts import (
    FINANCE_SYSTEM_PROMPT,
    build_forex_insight_prompt
)

from services.currency_service import (
    get_currency_for_destination,
    get_live_exchange_rate,
    convert_inr_to_destination
)

from services.llm_service import (
    LLMService
)


class ForexAgent:
    """
    AI Foreign Exchange Advisor.
    """

    def __init__(self):

        self.llm = LLMService()

    def analyze_forex(
        self,
        destination: str,
        budget: float
    ) -> dict:
        """
        Analyze exchange rate and generate
        forex recommendation.
        """

        destination_currency = (
            get_currency_for_destination(
                destination
            )
        )

        exchange_rate = (
            get_live_exchange_rate(
                "INR",
                destination_currency
            )
        )

        if exchange_rate is None:

            return {
                "success": False,
                "error": "Unable to fetch exchange rate."
            }

        converted_budget = (
            convert_inr_to_destination(
                budget,
                destination_currency
            )
        )

        prompt = (
            build_forex_insight_prompt(
                destination=destination,
                destination_currency=destination_currency,
                exchange_rate=exchange_rate,
                converted_budget=converted_budget
            )
        )

        response = self.llm.generate_response(
            system_prompt=FINANCE_SYSTEM_PROMPT,
            user_prompt=prompt,
            return_json=True
        )

        return {
            "success": True,
            "destination": destination,
            "currency": destination_currency,
            "exchange_rate": exchange_rate,
            "converted_budget": converted_budget,
            "analysis": response
        }