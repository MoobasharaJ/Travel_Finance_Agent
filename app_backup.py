import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

from utils.constants import (
    SUPPORTED_CURRENCIES,
    EXPENSE_CATEGORIES
)

from utils.calculations import (
    calculate_trip_duration,
    calculate_current_day,
    calculate_trip_progress
)

from services.forecasting_service import (
    generate_forecast
)

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="Travel Finance Agent",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Travel Finance Agent")

st.write(
    "An AI-powered travel companion for expense tracking, budgeting, and travel finance insights."
)

# =========================
# Session State
# =========================

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# =========================
# Trip Details
# =========================

st.header("🌍 Trip Details")

col1, col2 = st.columns(2)

with col1:

    destination = st.text_input(
        "Destination"
    )

    home_currency = st.selectbox(
        "Home Currency",
        SUPPORTED_CURRENCIES
    )

    budget = st.number_input(
        "Total Trip Budget",
        min_value=0.0,
        step=1000.0
    )

with col2:

    destination_currency = st.selectbox(
        "Destination Currency",
        SUPPORTED_CURRENCIES
    )

    trip_start_date = st.date_input(
        "Trip Start Date",
        value=date.today()
    )

    trip_end_date = st.date_input(
        "Trip End Date",
        value=date.today()
    )

# =========================
# Trip Calculations
# =========================

trip_duration = calculate_trip_duration(
    trip_start_date,
    trip_end_date
)

current_day = calculate_current_day(
    trip_start_date,
    trip_end_date
)

trip_progress_percent = calculate_trip_progress(
    current_day,
    trip_duration
)

# =========================
# Expense Entry
# =========================

st.divider()

st.header("💳 Add Expense")

col1, col2 = st.columns(2)

with col1:

    expense_category = st.selectbox(
        "Category",
        EXPENSE_CATEGORIES
    )

    expense_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0
    )

with col2:

    expense_currency = st.selectbox(
        "Currency",
        SUPPORTED_CURRENCIES
    )

    expense_description = st.text_input(
        "Description (Optional)"
    )

if st.button("Add Expense"):

    if expense_amount > 0:

        st.session_state.expenses.append(
            {
                "Category": expense_category,
                "Amount": expense_amount,
                "Currency": expense_currency,
                "Description": expense_description
            }
        )

        st.success(
            "Expense added successfully!"
        )

    else:

        st.warning(
            "Please enter a valid amount."
        )

# =========================
# Dashboard Calculations
# =========================

total_spent = sum(
    expense["Amount"]
    for expense in st.session_state.expenses
)

remaining_budget = (
    budget - total_spent
)

transaction_count = len(
    st.session_state.expenses
)

forecast = generate_forecast(
    budget=budget,
    total_spent=total_spent,
    current_day=current_day,
    trip_duration=trip_duration
)

# =========================
# Travel Dashboard
# =========================

st.divider()

st.header("📊 Travel Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Budget",
        f"{home_currency} {budget:,.0f}"
    )

with col2:
    st.metric(
        "Spent",
        f"{home_currency} {total_spent:,.0f}"
    )

with col3:
    st.metric(
        "Remaining",
        f"{home_currency} {remaining_budget:,.0f}"
    )

with col4:
    st.metric(
        "Current Day",
        f"{current_day}/{trip_duration}"
    )

# =========================
# Forecast Dashboard
# =========================

st.subheader("📈 Forecast Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Trip Progress",
        f"{forecast['trip_progress_percent']}%"
    )

with col2:
    st.metric(
        "Budget Used",
        f"{forecast['budget_used_percent']}%"
    )

with col3:
    st.metric(
        "Status",
        forecast["status"]
    )

# =========================
# Travel Finance Insight
# =========================

st.divider()

st.header("🧠 Travel Finance Insight")

if (
    budget > 0
    and trip_duration > 0
    and current_day > 0
):

    insight = (
        f"You are currently on Day {current_day} "
        f"of your trip to {destination}.\n\n"
        f"You have spent "
        f"{forecast['budget_used_percent']}% "
        f"of your budget while completing "
        f"{forecast['trip_progress_percent']}% "
        f"of your trip.\n\n"
    )

    if forecast["projected_difference"] < 0:

        insight += (
            f"⚠️ At the current spending rate, "
            f"you may exceed your budget by "
            f"{home_currency} "
            f"{abs(forecast['projected_difference']):,.0f}."
        )

    else:

        insight += (
            f"✅ At the current spending rate, "
            f"you are projected to remain within budget "
            f"and save approximately "
            f"{home_currency} "
            f"{forecast['projected_difference']:,.0f}."
        )

    st.info(insight)

else:

    st.info(
        "Add trip details and expenses "
        "to unlock travel finance insights."
    )

# =========================
# Spending Analysis
# =========================

if st.session_state.expenses:

    expense_df = pd.DataFrame(
        st.session_state.expenses
    )

    st.divider()

    st.header("📈 Spending Analysis")

    category_summary = (
        expense_df
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            by="Amount",
            ascending=False
        )
    )

    st.subheader(
        "Category Breakdown"
    )

    st.dataframe(
        category_summary,
        use_container_width=True
    )

    highest_category = (
        category_summary.iloc[0]["Category"]
    )

    highest_amount = (
        category_summary.iloc[0]["Amount"]
    )

    st.success(
        f"Highest spending category: "
        f"{highest_category} "
        f"({home_currency} {highest_amount:,.0f})"
    )

    fig, ax = plt.subplots()

    ax.pie(
        category_summary["Amount"],
        labels=category_summary["Category"],
        autopct="%1.1f%%"
    )

    ax.set_title(
        "Expense Distribution"
    )

    st.pyplot(fig)

# =========================
# Expense History
# =========================

st.divider()

st.header("📋 Expense History")

if st.session_state.expenses:

    expense_df = pd.DataFrame(
        st.session_state.expenses
    )

    st.dataframe(
        expense_df,
        use_container_width=True
    )

else:

    st.info(
        "No expenses added yet."
    )