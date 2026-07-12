"""
Finance Prompt Builder

Responsible for:
- Building prompts for Gemini

No API calls.
No calculations.
No business logic.
"""

def build_chat_prompt(summary, user_query):
    """
    Build prompt for AI chat.
    """

    trip = summary["trip"]
    analytics = summary["analytics"]

    return f"""
You are an AI Travel Finance Assistant.

Your purpose is to help travelers make smarter financial decisions and explore their destination.

==========================
TRIP DETAILS
==========================

Home Country: {trip['home_country']}
Destination: {trip['destination_country']}
Home Currency: {trip['home_currency']}
Destination Currency: {trip['destination_currency']}
Travel Budget ({trip['home_currency']}): {analytics['travel_budget']}
Total Spent: {analytics['total_expense']}
Remaining Budget ({trip['home_currency']}): {analytics['remaining_budget']}
Daily Allowance ({trip['home_currency']}): {analytics['daily_allowance']}
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
def build_dashboard_prompt(dashboard):
    """
    Build prompt for automatic dashboard insights.
    """

    trip = dashboard["trip"]
    analytics = dashboard["analytics"]
    forex = dashboard["forex"]

    return f"""
You are an intelligent Travel Finance Assistant.

Analyze the user's travel dashboard and provide concise financial advice based only on the available data.

Trip Details:
- Home Country: {trip['home_country']}
- Destination: {trip['destination_country']}
- Home Currency: {trip['home_currency']}
- Destination Currency: {trip['destination_currency']}
- Total Budget: {analytics['total_budget']}
- Travel Budget ({trip['home_currency']}): {analytics['travel_budget']}
- Total Spent: {analytics['total_expense']}
- Remaining Budget ({trip['home_currency']}): {analytics['remaining_budget']}
- Daily Allowance ({trip['home_currency']}): {analytics['daily_allowance']}
- Days Remaining: {analytics['days_remaining']}
- Trip Status: {analytics['trip_status']}

Forex:
Current Exchange Rate:
1 {trip['home_currency']} = {forex['live_rate']['exchange_rate']} {trip['destination_currency']}

- 7-Day Trend: {forex['7_day']['trend']}

Rules:
- Give ONLY 3 concise bullet points.
- Comment on the remaining budget.
- Comment on the daily allowance.
- Mention the forex trend if it affects travel decisions.
- Keep the advice practical.
- Do NOT repeat raw numbers unnecessarily.
- Maximum 70 words total.
"""

# ==========================================================
# Nearby Place Recommendation Prompt
# ==========================================================

def build_nearby_recommendation_prompt(
    dashboard,
    places,
    category,
):
    """
    Build prompt for ranking nearby places based on
    user's travel budget and forex.
    """

    trip = dashboard["trip"]
    analytics = dashboard["analytics"]
    forex = dashboard["forex"]

    places_text = ""

    for i, place in enumerate(places, start=1):

        places_text += f"""
{i}.

Name: {place["name"]}

Address: {place["address"]}

Rating: {place["rating"]}

Total Reviews: {place["total_ratings"]}

Google Maps:
{place["maps_url"]}

"""

    return f"""
You are a Smart Travel Finance Assistant.

Your job is to recommend ONLY the best nearby {category} that match the traveler's budget.

================================================
TRIP INFORMATION
================================================

Destination: {trip["destination_country"]}

Remaining Budget: {analytics["remaining_budget"]} {trip["home_currency"]}

Today's Safe Spending: {analytics["daily_allowance"]} {trip["home_currency"]}

Exchange Rate:
1 {trip["home_currency"]} = {forex["live_rate"]["exchange_rate"]} {trip["destination_currency"]}

================================================
NEARBY PLACES
================================================

{places_text}

================================================
YOUR TASK
================================================

Select ONLY the best 5 places.

Prioritize:
• Budget friendliness
• High ratings
• Good number of reviews
• Value for money
• Suitable for travelers
• Fits the user's remaining budget

For EACH place use EXACTLY this format:

### Place Name

⭐ Rating: X.X (if available)

================================================
RULES
================================================

• Maximum 5 recommendations.

• Maximum 1 sentence for "Why".

• Maximum 1 sentence for "Budget Fit".

• NO introductions.

• NO conclusions.

• NO travel history.

• NO long explanations.

• NO paragraphs.

• Keep the ENTIRE response under 150 words.

Return clean Markdown only.
"""