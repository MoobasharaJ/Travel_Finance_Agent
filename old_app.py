import pandas as pd
import streamlit as st
from datetime import date

import services.travel_service as ts

print("MODULE =", ts.__file__)

TravelService = ts.TravelService
from services.llm_service import LLMService

from prompts.finance_prompt import (
    build_dashboard_prompt,
    build_chat_prompt,
)

from utils.constants import (
    SUPPORTED_DESTINATIONS,
    PRE_TRIP_CATEGORIES,
    EXPENSE_CATEGORIES,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Travel Finance Agent",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Travel Finance Agent")
st.caption(
    "AI-powered Travel Budget Planning, Expense Tracking and Forex Intelligence"
)

# ==========================================================
# Services
# ==========================================================

travel_service = TravelService()
llm_service = LLMService()

# ==========================================================
# Session State
# ==========================================================

if "trip_id" not in st.session_state:
    st.session_state.trip_id = None

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("Travel Finance Agent")

st.sidebar.markdown("---")

if st.session_state.trip_id:

    dashboard = travel_service.get_dashboard_data(
        st.session_state.trip_id
    )

    trip = dashboard["trip"]

    st.sidebar.success("Current Trip")

    st.sidebar.write(
        f"**Destination:** {trip['destination']}"
    )

    st.sidebar.write(
        f"**Currency:** {trip['currency']}"
    )

    st.sidebar.write(
        f"**Duration:** {trip['duration']} Days"
    )

else:

    st.sidebar.info(
        "No trip created yet."
    )

# ==========================================================
# STEP 1 : CREATE TRIP
# ==========================================================

st.markdown("---")
st.header("Step 1 • Create Trip")

with st.form("trip_form"):

    destination = st.selectbox(
        "Destination",
        list(SUPPORTED_DESTINATIONS.keys())
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date"
        )

    with col2:
        end_date = st.date_input(
            "End Date"
        )

    total_budget = st.number_input(
        "Total Budget (INR)",
        min_value=0.0,
        step=1000.0
    )

    create_trip = st.form_submit_button(
        "Create Trip"
    )

if create_trip:

    if end_date < start_date:

        st.error(
            "End date must be after the start date."
        )

    elif total_budget <= 0:

        st.error(
            "Please enter a valid budget."
        )

    else:

        trip_id = travel_service.create_trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            total_budget=total_budget,
        )

        st.session_state.trip_id = trip_id

        st.success(
            "Trip created successfully!"
        )

        st.rerun()

    # ==========================================================
# STEP 2 : PRE-TRIP EXPENSES
# ==========================================================

if st.session_state.trip_id:

    st.markdown("---")
    st.header("Step 2 • Add Pre-trip Expenses")

    with st.form("pre_trip_form"):

        category = st.selectbox(
            "Category",
            PRE_TRIP_CATEGORIES
        )

        amount = st.number_input(
            "Amount (INR)",
            min_value=0.0,
            step=500.0
        )

        notes = st.text_input(
            "Notes (Optional)"
        )

        add_pre_trip = st.form_submit_button(
            "Add Pre-trip Expense"
        )

    if add_pre_trip:

        if amount <= 0:

            st.error("Please enter a valid amount.")

        else:

            travel_service.add_pre_trip_expense(
                trip_id=st.session_state.trip_id,
                category=category,
                amount=amount,
                notes=notes
            )

            st.success("Pre-trip expense added successfully!")

            st.rerun()

# ==========================================================
# STEP 3 : DASHBOARD
# ==========================================================

if st.session_state.trip_id:

    dashboard = travel_service.get_dashboard_data(
        st.session_state.trip_id
    )

    trip = dashboard["trip"]
    analytics = dashboard["analytics"]
    forex = dashboard["forex"]

    st.markdown("---")
    st.header("Step 3 • Dashboard")

    # ------------------------------------------------------
    # Budget Cards
    # ------------------------------------------------------

    st.subheader("Budget Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Destination",
            trip["destination"]
        )

        st.metric(
            "Total Budget",
            f"₹ {trip['total_budget']:,.2f}"
        )

        st.metric(
        "Travel Budget",
        f"₹ {trip['travel_budget']:,.2f}",
        f"≈ {dashboard['currency_conversion']['travel_budget']:.2f} {trip['currency']}"
        )

    with col2:
        st.metric(
            "Spent",
            f"₹ {analytics['total_expense']:,.2f}"
        )

        st.metric(
            "Remaining",
            f"₹ {analytics['remaining_budget']:,.2f}"
        )

    with col3:
        st.metric(
            "Daily Allowance",
            f"₹ {analytics['daily_allowance']:,.2f}"
        )

        st.metric(
            "Daily Average",
            f"₹ {analytics['daily_average']:,.2f}"
        )

    # ------------------------------------------------------
    # Analytics
    # ------------------------------------------------------

    st.subheader("Trip Analytics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Trip Progress",
            f"{analytics['trip_progress']} %"
        )

    with col2:

        st.metric(
            "Budget Used",
            f"{analytics['burn_rate']} %"
        )

    st.subheader("Category Breakdown")

    if analytics["category_breakdown"]:

        st.json(
            analytics["category_breakdown"]
        )

    else:

        st.info(
            "No travel expenses added yet."
        )

    # ------------------------------------------------------
    # Forex
    # ------------------------------------------------------

    st.subheader("Forex Intelligence")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            f"1 INR → {trip['currency']}",
            forex["live_rate"]["exchange_rate"]
        )

    with col2:

        st.metric(
            "7 Day Trend",
            forex["7_day"]["trend"]
        )

    with col3:

        st.metric(
            "30 Day Trend",
            forex["30_day"]["trend"]
        )

    with col4:

        st.metric(
            "90 Day Trend",
            forex["90_day"]["trend"]
        )

    # ------------------------------------------------------
    # AI Recommendation
    # ------------------------------------------------------

    st.subheader("AI Recommendation")

    dashboard_prompt = build_dashboard_prompt(
        dashboard
    )

    recommendation = llm_service.generate_response(
        dashboard_prompt
    )

    st.info(recommendation)

    # ==========================================================
# STEP 4 : DAILY EXPENSES
# ==========================================================

if st.session_state.trip_id:

    st.markdown("---")
    st.header("Step 4 • Add Daily Expense")

    with st.form("daily_expense_form"):

        expense_date = st.date_input(
            "Expense Date",
            value=date.today()
        )

        expense_category = st.selectbox(
            "Category",
            EXPENSE_CATEGORIES
        )

        expense_amount = st.number_input(
            "Amount (INR)",
            min_value=0.0,
            step=100.0,
            key="daily_amount"
        )

        expense_notes = st.text_input(
            "Notes (Optional)",
            key="daily_notes"
        )

        add_expense = st.form_submit_button(
            "Add Expense"
        )

    if add_expense:

        if expense_amount <= 0:

            st.error("Please enter a valid amount.")

        else:

            travel_service.add_expense(
                trip_id=st.session_state.trip_id,
                date=str(expense_date),
                category=expense_category,
                amount=expense_amount,
                notes=expense_notes
            )

            st.success("Expense added successfully!")

            st.rerun()

# ==========================================================
# STEP 5 : ASK AI
# ==========================================================

if st.session_state.trip_id:

    st.markdown("---")
    st.header("Step 5 • Ask AI")

    user_question = st.text_area(
        "Ask anything about your trip finances",
        placeholder="Example:\nCan I afford Disneyland?\nShould I exchange currency today?\nCan I spend ₹5000 on shopping?"
    )

    ask_ai = st.button("Ask AI")

    if ask_ai:

        if not user_question.strip():

            st.warning("Please enter a question.")

        else:

            dashboard = travel_service.get_dashboard_data(
                st.session_state.trip_id
            )

            prompt = build_chat_prompt(
                dashboard,
                user_question
            )

            with st.spinner("Thinking..."):

                response = llm_service.generate_response(
                    prompt
                )

            st.success(response)