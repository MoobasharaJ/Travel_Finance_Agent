"""
Prompt templates for all AI agents.
"""

FINANCE_SYSTEM_PROMPT = """
You are an expert Travel Finance Advisor.

Your job is to help travellers manage
their travel budget, expenses and
currency decisions.

Rules:

- Be concise.
- Be practical.
- Give actionable advice.
- Never invent numbers.
- Use only the provided information.
"""


def build_forex_insight_prompt(
    destination: str,
    destination_currency: str,
    exchange_rate: float,
    converted_budget: float
) -> str:
    """
    Prompt for Forex Agent.
    """

    return f"""
Destination:
{destination}

Currency:
{destination_currency}

Current Exchange Rate:
1 INR = {exchange_rate:.4f} {destination_currency}

Trip Budget:
{converted_budget:.2f} {destination_currency}

Tasks:

1. Write a short summary of the exchange rate.
2. Give one practical recommendation for the traveller.

The response MUST exactly follow this JSON format:

{{
    "summary": "string",
    "recommendation": "string"
}}

Do not include markdown.
Do not include code fences.
Do not include any extra text.
"""


def build_budget_insight_prompt(
    destination: str,
    cost_level: str,
    budget: float,
    spent: float,
    remaining: float,
    trip_progress: float,
    projected_spend: float
) -> str:
    """
    Prompt for Budget Agent.
    """

    return f"""
Destination:
{destination}

Cost Level:
{cost_level}

Budget:
{budget:.2f} INR

Spent:
{spent:.2f} INR

Remaining:
{remaining:.2f} INR

Trip Progress:
{trip_progress:.1f} %

Projected Total Spend:
{projected_spend:.2f} INR

Tasks:

1. Summarize the current budget status.
2. Assess the financial risk.
3. Suggest one practical recommendation.

Return ONLY this JSON:

{{
    "summary": "string",
    "risk_level": "Low | Medium | High",
    "recommendation": "string"
}}

Do not include markdown.
Do not include code fences.
Do not include any extra text.
"""


def build_expense_insight_prompt(
    total_spent: float,
    transaction_count: int,
    category_summary: str,
    highest_spending_category: str
) -> str:
    """
    Prompt for Expense Agent.
    """

    return f"""
Total Spent:
{total_spent:.2f} INR

Number of Transactions:
{transaction_count}

Category Breakdown:

{category_summary}

Highest Spending Category:
{highest_spending_category}


Tasks:

1. Identify the main spending pattern.
2. Mention one important observation.
3. Give one practical recommendation.


Return ONLY this JSON:

{{
    "summary": "string",
    "observation": "string",
    "recommendation": "string"
}}

Keep the response short.
Each value should be maximum 1-2 sentences.

Do not include markdown.
Do not include code fences.
Do not include any extra text.
"""