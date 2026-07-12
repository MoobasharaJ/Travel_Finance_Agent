# 🌍 Currency & Expense Travel Agent

An AI-powered travel finance assistant that helps international travelers plan budgets, track expenses, monitor exchange rates, and make smarter financial decisions throughout their journey.

---

## ✨ Overview

Managing travel expenses across different currencies can be challenging. Travelers often struggle with budgeting, fluctuating exchange rates, expense tracking, and finding budget-friendly services while abroad.

**Currency & Expense Travel Agent** simplifies travel finance by combining budget planning, expense tracking, live currency conversion, forex insights, AI-powered recommendations, and nearby place discovery into one intelligent application.

---

## 🚀 Features

### ✈️ Trip Planning
- Create and manage a trip
- Select home and destination countries
- Automatic currency detection
- Trip duration calculation
- Budget initialization

---

### 💰 Budget Planning
- Set total trip budget
- Record pre-trip expenses
  - Flights
  - Visa
  - Insurance
  - Forex Card
  - Shopping
  - Others
- Automatically calculate:
  - Travel Budget
  - Remaining Budget
  - Daily Safe Spending

---

### 💳 Expense Tracking
- Add travel expenses
- Separate Pre-trip and Travel expenses
- Categorized expense management
- Expense history
- Delete expenses
- Recent transaction management

---

### 💱 Currency & Forex Center
- Live exchange rates
- Currency conversion
- Historical exchange rate trends
- 7-Day analysis
- 30-Day analysis
- AI-powered forex insights

---

### 🤖 Smart Travel Assistant
Discover nearby:

- 🍽 Restaurants
- 🏧 ATMs
- 💱 Currency Exchange Centers
- 🛒 Convenience Stores

Powered by Google Places API with AI-curated recommendations based on:

- Budget
- Ratings
- Reviews
- Traveler convenience
- Value for money

---

### 💬 Ask AI
Ask travel finance questions such as:

- Can I afford this attraction?
- Where should I eat within my budget?
- Should I exchange currency today?
- How can I reduce my spending?
- Suggest a one-day itinerary.

---

### 📊 Dashboard Analytics

Visual insights including:

- Budget Overview
- Expense Breakdown
- Remaining Budget
- Daily Spending Allowance
- Currency Conversion
- Live Forex Snapshot
- AI Financial Insights

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- SQLite

### AI
- Google Gemini

### APIs
- Google Places API
- Exchange Rate API
- Frankfurter Historical Forex API

### Visualization
- Plotly

---

## 📂 Project Structure

```
currency-expense-travel-agent/

│
├── app.py
│
├── services/
│   ├── travel_service.py
│   ├── database_service.py
│   ├── currency_service.py
│   ├── forecasting_service.py
│   ├── google_places_service.py
│   └── llm_service.py
│
├── prompts/
│   └── finance_prompt.py
│
├── utils/
│   ├── calculations.py
│   └── constants.py
│
├── data/
│   └── travel.db
│
├── requirements.txt
└── README.md
```

---

## 🔄 Workflow

```text
Create Trip
      │
      ▼
Set Budget
      │
      ▼
Add Pre-trip Expenses
      │
      ▼
Travel Budget Calculated
      │
      ▼
Track Daily Expenses
      │
      ▼
Dashboard Analytics
      │
      ▼
Forex Monitoring
      │
      ▼
Smart Travel Assistant
      │
      ▼
Ask AI
```

## 🎯 Use Cases

- International Travelers
- Students studying abroad
- Business Travelers
- Solo Travelers
- Budget Travelers
- Vacation Planning

---

## 👨‍💻 Author

**Moobashara Jawed**

GitHub: https://github.com/MoobasharaJ

LinkedIn: https://www.linkedin.com/in/moobashara-jawed-84613a323/
