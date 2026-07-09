"""
Project-wide constants.

Travel Finance Agent
Version: 1.0
"""
GEMINI_MODEL = "gemini-flash-lite-latest"
# ==========================================================
# Supported Destinations
# ==========================================================

SUPPORTED_DESTINATIONS = {
    "United States": "USD",
    "United Kingdom": "GBP",
    "Japan": "JPY",
    "Singapore": "SGD",
    "Thailand": "THB",
    "United Arab Emirates": "AED",
    "Vietnam": "VND",
    "Indonesia": "IDR",
    "South Korea": "KRW",
    "Malaysia": "MYR",
    "Switzerland": "CHF",
    "Canada": "CAD",
    "Australia": "AUD",
    "France": "EUR",
    "Germany": "EUR",
    "Italy": "EUR",
    "Spain": "EUR",
    "Netherlands": "EUR",
    "Turkey": "TRY",
    "Sri Lanka": "LKR",
}

# ==========================================================
# Home Currency
# ==========================================================

HOME_CURRENCY = "INR"

# ==========================================================
# Pre-Trip Expense Categories
# ==========================================================

PRE_TRIP_CATEGORIES = [
    "Flight",
    "Visa",
    "Insurance",
    "Forex Card",
    "Shopping",
    "Others",
]

# ==========================================================
# During-Trip Expense Categories
# ==========================================================

EXPENSE_CATEGORIES = [
    "Food",
    "Hotel",
    "Transport",
    "Entertainment",
    "Medical",
    "Miscellaneous",
]

# ==========================================================
# Destination Cost Level
# Used for simple UI display
# ==========================================================

DESTINATION_COST_LEVEL = {
    "United States": "High",
    "United Kingdom": "High",
    "Japan": "High",
    "Singapore": "High",
    "Switzerland": "Very High",
    "Canada": "High",
    "Australia": "High",
    "France": "High",
    "Germany": "High",
    "Italy": "Medium",
    "Spain": "Medium",
    "Netherlands": "High",
    "United Arab Emirates": "Medium",
    "South Korea": "Medium",
    "Thailand": "Low",
    "Vietnam": "Low",
    "Indonesia": "Low",
    "Malaysia": "Low",
    "Turkey": "Low",
    "Sri Lanka": "Low",
}

# ==========================================================
# Forex Configuration
# ==========================================================

# ==========================================================
# Forex APIs
# ==========================================================

LIVE_FOREX_API_URL = "https://open.er-api.com/v6/latest"

HISTORICAL_FOREX_API_URL = "https://api.frankfurter.app"

# ==========================================================
# Historical Forex Windows
# ==========================================================

FOREX_WINDOWS = {
    "7D": 7,
    "30D": 30,
    "90D": 90,
}


# ==========================================================
# Database
# ==========================================================

DATABASE_PATH = "data/travel.db"

# ==========================================================
# Forecast Configuration
# ==========================================================

MIN_FORECAST_DAYS = 3

# ==========================================================
# Dashboard Labels
# ==========================================================

DASHBOARD_METRICS = [
    "Destination",
    "Total Budget",
    "Travel Budget",
    "Spent",
    "Remaining",
    "Daily Allowance",
    "Trip Progress",
    "Live Forex",
    "Forex Insight",
    "AI Recommendation",
]