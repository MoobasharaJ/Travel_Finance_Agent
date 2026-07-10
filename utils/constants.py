"""
Project-wide constants.

Travel Finance Agent
Version: 1.1
"""
GEMINI_MODEL = "gemini-flash-lite-latest"

# ==========================================================
# Supported Countries
# ==========================================================

SUPPORTED_COUNTRIES = {
    "Argentina": {"currency": "ARS"},
    "Australia": {"currency": "AUD"},
    "Austria": {"currency": "EUR"},
    "Belgium": {"currency": "EUR"},
    "Brazil": {"currency": "BRL"},
    "Canada": {"currency": "CAD"},
    "China": {"currency": "CNY"},
    "Denmark": {"currency": "DKK"},
    "Egypt": {"currency": "EGP"},
    "Finland": {"currency": "EUR"},
    "France": {"currency": "EUR"},
    "Germany": {"currency": "EUR"},
    "Greece": {"currency": "EUR"},
    "Hong Kong": {"currency": "HKD"},
    "India": {"currency": "INR"},
    "Indonesia": {"currency": "IDR"},
    "Ireland": {"currency": "EUR"},
    "Italy": {"currency": "EUR"},
    "Japan": {"currency": "JPY"},
    "Malaysia": {"currency": "MYR"},
    "Maldives": {"currency": "MVR"},
    "Mexico": {"currency": "MXN"},
    "Morocco": {"currency": "MAD"},
    "Nepal": {"currency": "NPR"},
    "Netherlands": {"currency": "EUR"},
    "New Zealand": {"currency": "NZD"},
    "Norway": {"currency": "NOK"},
    "Poland": {"currency": "PLN"},
    "Portugal": {"currency": "EUR"},
    "Qatar": {"currency": "QAR"},
    "Singapore": {"currency": "SGD"},
    "South Korea": {"currency": "KRW"},
    "Spain": {"currency": "EUR"},
    "Sri Lanka": {"currency": "LKR"},
    "Sweden": {"currency": "SEK"},
    "Switzerland": {"currency": "CHF"},
    "Taiwan": {"currency": "TWD"},
    "Thailand": {"currency": "THB"},
    "Turkey": {"currency": "TRY"},
    "United Arab Emirates": {"currency": "AED"},
    "United Kingdom": {"currency": "GBP"},
    "United States": {"currency": "USD"},
    "Vietnam": {"currency": "VND"},
}

# ==========================================================
# Expense Categories
# ==========================================================

EXPENSE_CATEGORIES = [
    "Flight",
    "Visa",
    "Insurance",
    "Accommodation",
    "Food",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Medical",
    "SIM/Internet",
    "Miscellaneous",
]

# ==========================================================
# Expense Types
# ==========================================================

PRE_TRIP = "PRE_TRIP"

TRAVEL = "TRAVEL"

EXPENSE_TYPES = [
    PRE_TRIP,
    TRAVEL,
]

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

