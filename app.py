import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date

from services.travel_service import TravelService
from services.llm_service import LLMService

from prompts.finance_prompt import (
    build_dashboard_prompt,
    build_chat_prompt,
    build_local_eateries_prompt,
    build_tourist_attractions_prompt,
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

if "eateries_result" not in st.session_state:
    st.session_state.eateries_result = None

if "tourist_result" not in st.session_state:
    st.session_state.tourist_result = None   


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

                    # Reset Explore Cache for new trip
                    st.session_state.eateries_result = None
                    st.session_state.tourist_result = None

                    # Optional: Clear previous AI answer
                    st.session_state.dashboard_ai = None

                    # Optional: Clear previous question
                    st.session_state.user_ai_query = ""

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

    # ======================================================
# Dashboard Header
# ======================================================

    st.header(f"🌍 {trip['destination']} Dashboard")

    status = analytics["trip_status"]

    if status == "Not Started":

       status_text = (
          f"🟢 Trip starts in "
          f"{analytics['days_until_trip']} day(s)"
        )

    elif status == "In Progress":

        current_day = min(
         analytics["days_elapsed"],
          trip["duration"]
        )

        status_text = (
           f"🟡 Day {current_day} "
           f"of {trip['duration']}"
        )

    else:

         status_text = "✅ Trip Completed"

    st.caption(
        f"📅 {trip['start_date']} → "
        f"{trip['end_date']} • "
        f"{trip['duration']} Days"
    )

    st.info(status_text)

    st.markdown("---")
    # ======================================================
# Currency View
# ======================================================

    st.subheader("💰 Budget Overview")

    currency_view = st.radio(
      "Display Currency",
       ["INR", trip["currency"]],
       horizontal=True,
       key="currency_view_radio"
    )

    if currency_view == "INR":

       currency_symbol = "₹"

       total_budget = trip["total_budget"]

       pre_trip = analytics["pre_trip_expenses"]

       travel_budget = trip["travel_budget"]

       spent = analytics["total_expense"]

       remaining = analytics["remaining_budget"]

       safe_spend = analytics["daily_allowance"]

       budget_used = analytics["burn_rate"]

    else:

       currency_symbol = trip["currency"]

       total_budget = conversion["total_budget"]

       pre_trip = conversion["pre_trip_expenses"]

       travel_budget = conversion["travel_budget"]

       spent = conversion["spent"]

       remaining = conversion["remaining_budget"]

       safe_spend = conversion["daily_allowance"]

       budget_used = analytics["burn_rate"]

# ======================================================
# Budget Flow
# ======================================================

    col1, arrow1, col2, arrow2, col3 = st.columns(
       [3, 0.5, 3, 0.5, 3]
    )

    with col1:

       st.metric(
        "💰 Total Budget",
        f"{currency_symbol} {total_budget:,.2f}"
       )

    with arrow1:

      st.markdown(
        "<h2 style='text-align:center;'>⬇️</h2>",
        unsafe_allow_html=True
      )

    with col2:

      st.metric(
        "✈️ Pre-trip Expenses",
        f"{currency_symbol} {pre_trip:,.2f}"
      )

    with arrow2:

      st.markdown(
        "<h2 style='text-align:center;'>⬇️</h2>",
        unsafe_allow_html=True
    )

    with col3:

      st.metric(
        "🎒 Travel Budget",
        f"{currency_symbol} {travel_budget:,.2f}"
      )

    st.caption(
      "Travel Budget = Total Budget − Pre-trip Expenses"
    )

    st.markdown("---")
    # ======================================================
# Current Spending
# ======================================================

    st.subheader("📊 Current Spending")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

       st.metric(
        "💸 Spent",
        f"{currency_symbol} {spent:,.2f}"
       )

    with col2:

      st.metric(
        "💰 Remaining",
        f"{currency_symbol} {remaining:,.2f}"
      )

    with col3:

      st.metric(
        "📈 Budget Used",
        f"{budget_used:.1f}%"
      )

    with col4:

      if analytics["trip_status"] == "Not Started":

        st.metric(
            "🗓 Trip Starts In",
            f"{analytics['days_until_trip']} Day(s)"
        )

      elif analytics["trip_status"] == "In Progress":

        st.metric(
            "💵 Today's Safe Spend",
            f"{currency_symbol} {safe_spend:,.2f}"
        )

      else:

        st.metric(
            "✅ Status",
            "Trip Completed"
        )

    st.markdown("---")

    # ======================================================
# Forex Snapshot
# ======================================================

    st.subheader("📈 Forex Snapshot")

    col1, col2 = st.columns([3, 1])

    with col1:

     st.metric(
        "Live Exchange Rate",
        f"1 INR = {forex['live_rate']['exchange_rate']} {trip['currency']}"
    )

    with col2:

      trend = forex["30_day"].get("trend", "Unavailable")

      if trend == "Up":
       st.success("🟢 Good time to exchange")

      elif trend == "Down":
       st.warning("🟡 Monitor exchange rate")

      elif trend == "Stable":
       st.info("⚪ Stable trend")

      else:
       st.info("⚪ Historical trend unavailable")

    st.caption(
    "For detailed exchange rate analysis, visit Forex Center."
    )

    st.markdown("---")

    # ======================================================
# Expense Breakdown
# ======================================================

    st.subheader("📊 Expense Breakdown")

    breakdown = analytics["category_breakdown"]

    if breakdown:

      df = pd.DataFrame(

        list(breakdown.items()),

        columns=[
            "Category",
            "Amount"
        ]
       )

      fig = px.pie(

        df,

        names="Category",

        values="Amount",

        hole=0.45,

        title="Travel Expenses by Category"
       )

      fig.update_layout(
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
      )

      st.plotly_chart(
        fig,
        use_container_width=True
      )

    if analytics["top_spending_category"]:

        st.info(
            f"💡 Highest spending category: "
            f"**{analytics['top_spending_category']}**"
        )

    else:

      st.info(
        "No travel expenses yet.\n\n"
        "Start tracking expenses to visualize your spending."
    )

    st.markdown("---")

    # ======================================================
# Smart Insights
# ======================================================

    st.subheader("💡 Smart Insights")

    if st.session_state.dashboard_ai is None:

      prompt = build_dashboard_prompt(dashboard)

      with st.spinner("Analyzing your trip..."):

        st.session_state.dashboard_ai = (
            llm_service.generate_response(prompt)
        )

    st.success(st.session_state.dashboard_ai)
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
# Explore & Ask AI
# ==========================================================

# ==========================================================
# Explore & Ask AI
# ==========================================================

def show_ai():

    st.header("✨ Explore Your Destination")

    st.caption(
        "Smart recommendations tailored for your destination."
    )

    if st.session_state.trip_id is None:

        st.warning("Please create a trip first.")

        return

    # ------------------------------------------------------
    # Dashboard Data
    # ------------------------------------------------------

    summary = travel_service.get_trip_summary(
    st.session_state.trip_id
    )

    trip = summary["trip"]

    analytics = summary["analytics"]

    # ======================================================
    # Local Eateries
    # ======================================================

    with st.expander(
        "🍜 **Local Eateries**\n\nDiscover authentic local flavours",
        expanded=False
    ):

        if st.session_state.eateries_result is None:

            with st.spinner(
                "Finding authentic local eateries..."
            ):

                prompt = build_local_eateries_prompt(
                    trip["destination"]
                )

                st.session_state.eateries_result = (
                    llm_service.generate_response(prompt)
                )

        st.markdown(
            st.session_state.eateries_result
        )

    # ======================================================
    # Tourist Attractions
    # ======================================================

    with st.expander(
        "🏛 **Tourist Attractions**\n\nDiscover iconic attractions & hidden gems",
        expanded=False
    ):

        if st.session_state.tourist_result is None:

            with st.spinner(
                "Finding popular attractions..."
            ):

                prompt = build_tourist_attractions_prompt(
                    trip["destination"]
                )

                st.session_state.tourist_result = (
                    llm_service.generate_response(prompt)
                )

        st.markdown(
            st.session_state.tourist_result
        )

    st.markdown("---")

    # ======================================================
    # Ask AI
    # ======================================================
    st.subheader("🤖 Ask AI")

    user_query = st.text_area(
        "Ask anything about your trip",
        height=120,
        placeholder="Example: Can I afford a day trip to Mount Fuji?",
        key="user_ai_query"
    )

    if st.button(
        "Get AI Advice",
        use_container_width=True
    ):

        if not user_query.strip():

            st.warning(
                "Please enter your question."
            )

        else:

            with st.spinner(
                "Analyzing your trip..."
            ):

                prompt = build_chat_prompt(
                    dashboard,
                    user_query
                )

                response = llm_service.generate_response(
                    prompt
                )

            st.markdown("---")

            st.subheader("💡 AI Travel Advice")

            with st.container(border=True):

                st.markdown(response)
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
