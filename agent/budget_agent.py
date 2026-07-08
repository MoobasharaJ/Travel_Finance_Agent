"""
Budget Agent

Responsible for:

- Budget health analysis
- Forecast interpretation
- Budget coaching recommendations
"""

from prompts.finance_prompts import (
    FINANCE_SYSTEM_PROMPT,
    build_budget_insight_prompt
)

from services.llm_service import (
    LLMService
)


class BudgetAgent:
    """
    AI Budget Coach.
    """

    def __init__(self):

        self.llm = LLMService()


    def analyze_budget(
        self,
        destination: str,
        cost_level: str,
        budget: float,
        total_spent: float,
        trip_progress_percent: float,
        projected_total_spend: float
    ) -> dict:
        """
        Analyze budget using Gemini.

        Parameters:
        - destination: Travel destination
        - cost_level: Low / Medium / High cost destination
        - budget: Total trip budget in INR
        - total_spent: Amount already spent in INR
        - trip_progress_percent: Percentage of trip completed
        - projected_total_spend: Expected final spending
        """

        remaining = budget - total_spent


        prompt = build_budget_insight_prompt(
            destination=destination,
            cost_level=cost_level,
            budget=budget,
            spent=total_spent,
            remaining=remaining,
            trip_progress=trip_progress_percent,
            projected_spend=projected_total_spend
        )


        response = self.llm.generate_response(
            system_prompt=FINANCE_SYSTEM_PROMPT,
            user_prompt=prompt,
            return_json=True
        )


        return {
            "success": True,
            "destination": destination,
            "budget": budget,
            "spent": total_spent,
            "remaining": remaining,
            "analysis": response
        }