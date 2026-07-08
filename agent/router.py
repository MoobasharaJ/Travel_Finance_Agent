"""
Travel Finance Router

Responsible for:

- Understanding the user's request
- Routing the request to the correct AI agent
- Returning a unified response
"""


from pandas import DataFrame

from services.llm_service import LLMService

from agent.forex_agent import ForexAgent
from agent.budget_agent import BudgetAgent
from agent.expense_agent import ExpenseAgent


ROUTER_SYSTEM_PROMPT = """
You are an AI intent classifier.

Your task is to classify the user's request.

Possible intents:

- forex
- budget
- expense
- full_report

Rules:

Return ONLY valid JSON.

Example:

{
    "intent":"forex"
}
"""


class TravelFinanceRouter:

    def __init__(self):

        self.llm = LLMService()

        self.forex_agent = ForexAgent()
        self.budget_agent = BudgetAgent()
        self.expense_agent = ExpenseAgent()

    def _detect_intent(
        self,
        user_query: str
    ) -> str:

        prompt = f"""
User Request:

{user_query}

Return ONLY:

{{
    "intent":"forex | budget | expense | full_report"
}}
"""

        response = self.llm.generate_response(
            system_prompt=ROUTER_SYSTEM_PROMPT,
            user_prompt=prompt,
            return_json=True
        )

        if not isinstance(response, dict):
            return "full_report"

        return response.get(
            "intent",
            "full_report"
        )

    def generate_report(
        self,
        user_query: str,
        destination: str,
        cost_level: str,
        budget: float,
        total_spent: float,
        trip_progress_percent: float,
        projected_total_spend: float,
        category_summary: DataFrame,
        highest_spending_category: str,
        transaction_count: int
    ) -> dict:

        intent = self._detect_intent(
            user_query
        )

        report = {
            "intent": intent
        }

        if intent in ["forex", "full_report"]:

            report["forex"] = (
                self.forex_agent.analyze_forex(
                    destination,
                    budget
                )
            )

        if intent in ["budget", "full_report"]:

            report["budget"] = (
                self.budget_agent.analyze_budget(
                    destination=destination,
                    cost_level=cost_level,
                    budget=budget,
                    total_spent=total_spent,
                    trip_progress_percent=trip_progress_percent,
                    projected_total_spend=projected_total_spend
                )
            )

        if intent in ["expense", "full_report"]:

            report["expense"] = (
                self.expense_agent.analyze_expenses(
                    total_spent=total_spent,
                    transaction_count=transaction_count,
                    category_summary=category_summary,
                    highest_spending_category=highest_spending_category
                )
            )

        return report