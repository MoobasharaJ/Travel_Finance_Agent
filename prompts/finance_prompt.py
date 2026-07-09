"""
Finance Prompt Builder

Responsible for:
- Building prompts for Gemini

No API calls.
No calculations.
No business logic.
"""

import json


def build_dashboard_prompt(dashboard_data):
    """
    Build prompt for automatic dashboard financial advice.
    """

    dashboard_json = json.dumps(dashboard_data, indent=2)

    return f"""
You are an AI Travel Finance Advisor.

Your role is to explain the user's financial situation during their trip.

Below is the complete dashboard data.

Dashboard Data
--------------
{dashboard_json}

Instructions
------------
- Use ONLY the provided information.
- Never perform calculations.
- Never invent numbers.
- Never predict future exchange rates.
- Explain what the forex trend means.
- Mention whether spending appears healthy.
- Mention if the remaining budget seems sufficient.
- Give practical travel finance advice.
- Keep the response under 120 words.
"""


def build_chat_prompt(dashboard, user_query):
    """
    Build prompt for AI chat.
    """

    trip = dashboard["trip"]
    analytics = dashboard["analytics"]
    forex = dashboard["forex"]

    return f"""
You are an AI Travel Finance Assistant.

Your purpose is to help travelers make smarter financial decisions and explore their destination.

==========================
TRIP DETAILS
==========================

Destination: {trip['destination']}
Currency: {trip['currency']}
Travel Budget: {trip['travel_budget']}
Total Spent: {analytics['total_expense']}
Remaining Budget: {analytics['remaining_budget']}
Daily Allowance: {analytics['daily_allowance']}

==========================
FOREX
==========================

Current Exchange Rate:
1 INR = {forex['live_rate']['exchange_rate']} {trip['currency']}

7-Day Trend:
{forex['7_day']}

30-Day Trend:
{forex['30_day']}

==========================
RULES
==========================

1. If the question is related to budget, expenses or forex,
ALWAYS use the dashboard information.

2. If the user asks about restaurants, attractions,
shopping, transport, hotels, trip cost or any destination
information that is NOT available in the dashboard,
use your own travel knowledge.

3. Whenever you mention prices,
clearly state that they are approximate estimates.

4. If enough budget information is available,
tell the user whether the activity appears affordable.

5. Keep answers concise and practical.

6. Do NOT answer unrelated questions.

==========================

User Question:

{user_query}
"""
# ==========================================================
# Explore Destination Prompts
# ==========================================================

def build_local_eateries_prompt(destination: str) -> str:
    """
    Prompt for recommending authentic local eateries.
    """

    return f"""
You are an expert travel guide.

Destination:
{destination}

Recommend EXACTLY 5 authentic local eateries that are popular with locals and tourists.

For EVERY recommendation use EXACTLY this format:

### 🍜 <Restaurant Name>

**Budget:** 🟢 Budget / 🟡 Moderate / 🔴 Premium

**Approx Cost:**
<Cost per person in local currency>

**Famous For:**
<One short line>

---

Rules:

• Recommend ONLY authentic local places.
• Avoid international fast-food chains.
• Keep every recommendation under 3 lines.
• No introduction.
• No conclusion.
• No extra explanation.
• Return ONLY the recommendations.
"""


def build_tourist_attractions_prompt(destination: str) -> str:
    """
    Prompt for recommending tourist attractions.
    """

    return f"""
You are an expert travel guide.

Destination:
{destination}

Recommend EXACTLY 5 tourist attractions.

Include:
• Famous attractions
• Hidden gems

For EVERY recommendation use EXACTLY this format:

### 🏛 <Attraction Name>

**Budget:** 🟢 Free / 🟡 Moderate / 🔴 Premium

**Approx Entry Fee:**
<Entry fee in local currency or Free>

**Why Visit:**
<One short line>

---

Rules:

• Keep every recommendation under 3 lines.
• No introduction.
• No conclusion.
• No extra explanation.
• Return ONLY the recommendations.
"""