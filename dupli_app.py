import streamlit as st
import pandas as pd
from datetime import date

from services.travel_service import TravelService
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
    layout="wide",
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

if "dashboard_ai" not in st.session_state:
    st.session_state.dashboard_ai = None

if "currency_view" not in st.session_state:
    st.session_state.currency_view = "INR"

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("✈️ Travel Finance Agent")

    st.markdown("---")

    if st.session_state.trip_id:

        trip = travel_service.db.get_trip(
            st.session_state.trip_id
        )

        st.subheader("Current Trip")

        st.write(f"📍 {trip['destination']}")
        st.write(f"💱 {trip['currency']}")
        st.write(
            f"🗓️ {trip['start_date']} → {trip['end_date']}"
        )

        st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Expenses",
            "Forex Center",
            "Ask AI",
        ]
    )

st.title("Travel Finance Agent")

# ==========================================================
# Dashboard
# ==========================================================

def show_dashboard():

    st.header("Dashboard")

    # ------------------------------------------------------
    # No Trip Created
    # ------------------------------------------------------

    if st.session_state.trip_id is None:

        st.info("Create a trip to get started.")

        with st.form("create_trip_form"):

            col1, col2 = st.columns(2)

            with col1:

                destination = st.selectbox(
                    "Destination",
                    options=list(SUPPORTED_DESTINATIONS.keys()),
                    index=None,
                    placeholder="Select Destination",
                )

                total_budget = st.number_input(
                    "Total Budget (INR)",
                    min_value=0.0,
                    step=1000.0,
                )

            with col2:

                start_date = st.date_input(
                    "Start Date",
                    value=date.today()
                )

                end_date = st.date_input(
                    "End Date",
                    value=date.today()
                )

            submitted = st.form_submit_button(
                "Create Trip",
                use_container_width=True
            )

            if submitted:

                if destination is None:

                    st.error("Please select a destination.")

                elif end_date < start_date:

                    st.error(
                        "End date cannot be before start date."
                    )

                elif total_budget <= 0:

                    st.error(
                        "Budget should be greater than zero."
                    )

                else:

                    trip_id = travel_service.create_trip(
                        destination,
                        start_date,
                        end_date,
                        total_budget
                    )

                    st.session_state.trip_id = trip_id

                    st.success("Trip created successfully!")

                    st.rerun()

        return

    # ------------------------------------------------------
    # Existing Trip
    # ------------------------------------------------------

    dashboard = travel_service.get_dashboard_data(
        st.session_state.trip_id
    )

    trip = dashboard["trip"]

    analytics = dashboard["analytics"]

    forex = dashboard["forex"]

    conversion = dashboard["currency_conversion"]

    st.subheader(
        f"{trip['destination']} Trip"
    )

        # ======================================================
    # Currency Toggle
    # ======================================================

    st.markdown("### Budget Overview")

    currency_view = st.radio(
        "Display Currency",
        ["INR", trip["currency"]],
        horizontal=True,
        key="currency_view_radio"
    )

    if currency_view == "INR":

        budget = trip["travel_budget"]
        spent = analytics["total_expense"]
        remaining = analytics["remaining_budget"]
        safe_spend = analytics["daily_allowance"]
        currency_symbol = "₹"

    else:

        budget = conversion["travel_budget"]
        spent = budget - conversion["remaining_budget"]
        remaining = conversion["remaining_budget"]
        safe_spend = conversion["remaining_budget"]

        currency_symbol = trip["currency"]

    # ======================================================
    # Budget Cards
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Travel Budget",
            f"{currency_symbol} {budget:,.2f}"
        )

    with col2:
        st.metric(
            "Spent",
            f"{currency_symbol} {spent:,.2f}"
        )

    with col3:
        st.metric(
            "Remaining",
            f"{currency_symbol} {remaining:,.2f}"
        )

    with col4:
        st.metric(
            "Today's Safe Spend",
            f"{currency_symbol} {safe_spend:,.2f}"
        )

    st.markdown("---")

    # ======================================================
    # Forex Snapshot
    # ======================================================

    st.subheader("📈 Forex Snapshot")

    forex_col1, forex_col2 = st.columns([2, 1])

    with forex_col1:

        st.metric(
            "Live Exchange Rate",
            f"1 INR = {forex['live_rate']['exchange_rate']} {trip['currency']}"
        )

        st.info(
            "Open **Forex Center** from the sidebar for detailed "
            "7-Day and 30-Day trend analysis."
        )

    with forex_col2:

        trend = forex["7_day"]["trend"]

        if trend == "Up":
            st.success("🟢 Favorable")

        elif trend == "Down":
            st.warning("🟡 Watch Rate")

        else:
            st.info("⚪ Stable")

    st.markdown("---")

    # ======================================================
    # AI Recommendation
    # ======================================================

    st.subheader("🤖 AI Recommendation")

    if st.button("Generate Recommendation"):

        with st.spinner("Analyzing your trip..."):

            prompt = build_dashboard_prompt(dashboard)

            st.session_state.dashboard_ai = (
                llm_service.generate_response(prompt)
            )

    if st.session_state.dashboard_ai:

        st.success(
            st.session_state.dashboard_ai
        )

    # ==========================================================
# Expenses Page
# ==========================================================

def show_expenses():

    st.header("Expenses")

    if st.session_state.trip_id is None:

        st.warning("Please create a trip first.")

        return

    # ======================================================
    # Pre-Trip Expenses
    # ======================================================

    st.subheader("Pre-trip Expenses")

    with st.form("pre_trip_form"):

        col1, col2 = st.columns(2)

        with col1:

            category = st.selectbox(
                "Category",
                PRE_TRIP_CATEGORIES,
                index=None,
                placeholder="Select Category"
            )

        with col2:

            amount = st.number_input(
                "Amount (INR)",
                min_value=0.0,
                step=100.0
            )

        notes = st.text_input("Notes (Optional)")

        submitted = st.form_submit_button(
            "Add Pre-trip Expense",
            use_container_width=True
        )

        if submitted:

            if category is None:

                st.error("Please select a category.")

            elif amount <= 0:

                st.error("Enter a valid amount.")

            else:

                travel_service.add_pre_trip_expense(
                    st.session_state.trip_id,
                    category,
                    amount,
                    notes
                )

                st.success("Expense added successfully.")

                st.rerun()

    # ======================================================
    # Pre-trip Expense History
    # ======================================================

    st.markdown("### Expense History")

    history = travel_service.db.get_pre_trip_expenses(
        st.session_state.trip_id
    )

    if history:

        df = pd.DataFrame(history)

        st.dataframe(
            df[
                [
                    "category",
                    "amount",
                    "notes"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info("No pre-trip expenses added.")

    st.markdown("---")

    # ======================================================
    # Daily Expenses
    # ======================================================

    st.subheader("Daily Expenses")

    with st.form("daily_expense_form"):

        col1, col2 = st.columns(2)

        with col1:

            expense_date = st.date_input(
                "Expense Date",
                value=date.today()
            )

            expense_category = st.selectbox(
                "Category",
                EXPENSE_CATEGORIES,
                index=None,
                placeholder="Select Category"
            )

        with col2:

            expense_amount = st.number_input(
                "Amount",
                min_value=0.0,
                step=100.0
            )

            expense_notes = st.text_input(
                "Notes"
            )

        submitted = st.form_submit_button(
            "Add Daily Expense",
            use_container_width=True
        )

        if submitted:

            if expense_category is None:

                st.error("Please select a category.")

            elif expense_amount <= 0:

                st.error("Enter a valid amount.")

            else:

                travel_service.add_expense(
                    st.session_state.trip_id,
                    expense_date,
                    expense_category,
                    expense_amount,
                    expense_notes
                )

                st.success("Expense added successfully.")

                st.rerun()

    # ======================================================
    # Daily Expense History
    # ======================================================

    st.markdown("### Daily Expense History")

    expenses = travel_service.db.get_expenses(
        st.session_state.trip_id
    )

    if expenses:

        df = pd.DataFrame(expenses)

        st.dataframe(
            df[
                [
                    "date",
                    "category",
                    "amount",
                    "notes"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info("No daily expenses added.")

    # ==========================================================
# Forex Center
# ==========================================================

def show_forex():

    st.header("📈 Forex Center")

    if st.session_state.trip_id is None:

        st.warning("Please create a trip first.")

        return

    dashboard = travel_service.get_dashboard_data(
        st.session_state.trip_id
    )

    trip = dashboard["trip"]
    forex = dashboard["forex"]

    # ======================================================
    # Live Exchange Rate
    # ======================================================

    st.subheader("Live Exchange Rate")

    st.metric(
        f"1 INR",
        f"{forex['live_rate']['exchange_rate']} {trip['currency']}"
    )

    st.markdown("---")

    # ======================================================
    # Historical Comparison
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        trend7 = forex["7_day"]

        st.subheader("Last 7 Days")

        st.metric(
            "Current Rate",
            trend7["current_rate"]
        )

        st.write(
            f"Average : {trend7['moving_average']}"
        )

        st.write(
            f"Change : {trend7['percentage_change']} %"
        )

        if trend7["trend"] == "Up":
            st.success("🟢 Rate Improved")

        elif trend7["trend"] == "Down":
            st.warning("🟡 Rate Weakened")

        else:
            st.info("⚪ Stable")

    with col2:

        trend30 = forex["30_day"]

        st.subheader("Last 30 Days")

        st.metric(
            "Current Rate",
            trend30["current_rate"]
        )

        st.write(
            f"Average : {trend30['moving_average']}"
        )

        st.write(
            f"Change : {trend30['percentage_change']} %"
        )

        if trend30["trend"] == "Up":
            st.success("🟢 Rate Improved")

        elif trend30["trend"] == "Down":
            st.warning("🟡 Rate Weakened")

        else:
            st.info("⚪ Stable")

    st.markdown("---")

    # ======================================================
    # Forex Insight
    # ======================================================

    st.subheader("Forex Insight")

    if trend7["current_rate"] < trend7["moving_average"]:

        st.success(
            "Today's exchange rate is below the "
            "7-day average.\n\n"
            "This appears to be a relatively "
            "better time to exchange currency."
        )

    else:

        st.info(
            "Today's exchange rate is above the "
            "7-day average.\n\n"
            "If your exchange is not urgent, "
            "you may consider waiting."
        )

    st.markdown("---")

    # ======================================================
    # Currency Converter
    # ======================================================

    st.subheader("Currency Converter")

    amount = st.number_input(
        f"Amount ({trip['currency']})",
        min_value=0.0,
        step=100.0,
    )

    converted = amount / forex["live_rate"]["exchange_rate"]

    st.metric(
        "Equivalent INR",
        f"₹ {converted:,.2f}"
    )    
    # ==========================================================
# Ask AI
# ==========================================================

def show_ai():

    st.header("🤖 Ask AI")

    if st.session_state.trip_id is None:

        st.warning("Please create a trip first.")

        return

    dashboard = travel_service.get_dashboard_data(
        st.session_state.trip_id
    )

    user_query = st.text_area(
        "Ask your travel finance question",
        placeholder="Example:\n\nCan I afford Disneyland?\nShould I exchange currency today?\nHow much can I spend on shopping?"
    )

    if st.button(
        "Ask AI",
        use_container_width=True
    ):

        if user_query.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                prompt = build_chat_prompt(
                    dashboard,
                    user_query
                )

                response = llm_service.generate_response(
                    prompt
                )

            st.markdown("### AI Response")

            st.success(response)


# ==========================================================
# Navigation
# ==========================================================

if page == "Dashboard":

    show_dashboard()

elif page == "Expenses":

    show_expenses()

elif page == "Forex Center":

    show_forex()

elif page == "Ask AI":

    show_ai()