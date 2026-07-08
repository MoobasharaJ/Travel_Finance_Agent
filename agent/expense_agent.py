"""
Expense Agent

Responsible for:

- Expense pattern analysis
- Spending behaviour insights
- Expense recommendations
"""

from pandas import DataFrame

from prompts.finance_prompts import (
    FINANCE_SYSTEM_PROMPT,
    build_expense_insight_prompt
)

from services.llm_service import (
    LLMService
)


class ExpenseAgent:
    """
    AI Expense Assistant.
    """

    def __init__(self):

        self.llm = LLMService()


    def _format_category_summary(
        self,
        category_summary: DataFrame
    ) -> str:
        """
        Convert category summary DataFrame
        into readable text for the LLM.
        """

        if category_summary.empty:
            return "No expense data available."


        lines = []

        for _, row in category_summary.iterrows():

            lines.append(
                f"{row['Category']}: "
                f"{row['Amount']:.2f} INR"
            )

        return "\n".join(lines)



    def analyze_expenses(
        self,
        total_spent: float,
        transaction_count: int,
        category_summary: DataFrame,
        highest_spending_category: str
    ) -> dict:
        """
        Analyze expense data using Gemini.
        """


        formatted_summary = (
            self._format_category_summary(
                category_summary
            )
        )


        prompt = build_expense_insight_prompt(
            total_spent=total_spent,
            transaction_count=transaction_count,
            category_summary=formatted_summary,
            highest_spending_category=highest_spending_category
        )


        response = self.llm.generate_response(
            system_prompt=FINANCE_SYSTEM_PROMPT,
            user_prompt=prompt,
            return_json=True
        )


        return {
            "success": True,
            "total_spent": total_spent,
            "transaction_count": transaction_count,
            "highest_spending_category": highest_spending_category,
            "analysis": response
        }