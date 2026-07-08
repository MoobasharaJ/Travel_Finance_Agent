"""
Project-wide constants.

Travel Finance Agent
V1 Prototype
"""

# =========================
# Supported Currencies
# =========================

SUPPORTED_CURRENCIES = [
    "INR",
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "SGD",
    "THB",
    "AED",
    "VND",
    "IDR",
    "KRW",
    "MYR",
    "CHF",
    "CAD",
    "AUD",
    "NZD",
    "ZAR"
]


# =========================
# Supported Destinations
# =========================

SUPPORTED_DESTINATIONS = [
    "Japan",
    "Thailand",
    "Singapore",
    "Indonesia",
    "Vietnam",
    "Malaysia",
    "South Korea",
    "United Arab Emirates",
    "France",
    "Germany",
    "Italy",
    "Spain",
    "Switzerland",
    "United Kingdom",
    "Netherlands",
    "United States",
    "Canada",
    "Australia",
    "New Zealand",
    "South Africa"
]


# =========================
# Destination → Currency
# =========================

DESTINATION_TO_CURRENCY = {
    "Japan": "JPY",
    "Thailand": "THB",
    "Singapore": "SGD",
    "Indonesia": "IDR",
    "Vietnam": "VND",
    "Malaysia": "MYR",
    "South Korea": "KRW",
    "United Arab Emirates": "AED",
    "France": "EUR",
    "Germany": "EUR",
    "Italy": "EUR",
    "Spain": "EUR",
    "Switzerland": "CHF",
    "United Kingdom": "GBP",
    "Netherlands": "EUR",
    "United States": "USD",
    "Canada": "CAD",
    "Australia": "AUD",
    "New Zealand": "NZD",
    "South Africa": "ZAR"
}


# =========================
# Destination Intelligence
# =========================

COUNTRY_PROFILES = {

    "Japan": {
        "cost_level": "High"
    },

    "Thailand": {
        "cost_level": "Low"
    },

    "Singapore": {
        "cost_level": "High"
    },

    "Indonesia": {
        "cost_level": "Low"
    },

    "Vietnam": {
        "cost_level": "Low"
    },

    "Malaysia": {
        "cost_level": "Medium"
    },

    "South Korea": {
        "cost_level": "High"
    },

    "United Arab Emirates": {
        "cost_level": "High"
    },

    "France": {
        "cost_level": "High"
    },

    "Germany": {
        "cost_level": "High"
    },

    "Italy": {
        "cost_level": "High"
    },

    "Spain": {
        "cost_level": "Medium"
    },

    "Switzerland": {
        "cost_level": "Very High"
    },

    "United Kingdom": {
        "cost_level": "High"
    },

    "Netherlands": {
        "cost_level": "High"
    },

    "United States": {
        "cost_level": "High"
    },

    "Canada": {
        "cost_level": "High"
    },

    "Australia": {
        "cost_level": "High"
    },

    "New Zealand": {
        "cost_level": "High"
    },

    "South Africa": {
        "cost_level": "Medium"
    }
}


# =========================
# Expense Categories
# =========================

EXPENSE_CATEGORIES = [
    "Food",
    "Accommodation",
    "Transport",
    "Shopping",
    "Entertainment",
    "Miscellaneous"
]


# =========================
# Pre-Trip Expenses
# =========================

PRE_TRIP_EXPENSE_CATEGORIES = [
    "Flight",
    "Visa",
    "Insurance"
]


# =========================
# Dashboard Messages
# =========================

DEFAULT_INSIGHT_MESSAGE = (
    "Add trip details and expenses "
    "to generate travel insights."
)


# =========================
# Budget Status Labels
# =========================

STATUS_ON_TRACK = "On Track"

STATUS_WARNING = "Warning"

STATUS_OVERSPENDING = "Overspending"


# =========================
# Forecast Thresholds
# =========================

WARNING_THRESHOLD_PERCENT = 80

CRITICAL_THRESHOLD_PERCENT = 100


# =========================
# Database
# =========================

DATABASE_NAME = "data/expenses.db"


# =========================
# Currency API
# =========================

EXCHANGE_RATE_BASE_URL = (
    "https://open.er-api.com/v6/latest"
)


# =========================
# AI Assistant
# =========================

MAX_CHAT_HISTORY = 10