import streamlit as st

st.set_page_config(
    page_title="Travel Finance Agent",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Travel Finance Agent")

st.write(
    "An AI-powered travel companion for expense tracking, budgeting and currency intelligence."
)

st.header("Trip Details")

budget = st.number_input(
    "Total Trip Budget",
    min_value=0.0,
    step=1000.0
)

destination = st.text_input(
    "Destination Country"
)

trip_days = st.number_input(
    "Trip Duration (Days)",
    min_value=1,
    step=1
)

st.divider()

st.header("Trip Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Budget", f"₹{budget:,.0f}")

with col2:
    st.metric(
        "Destination",
        destination if destination else "-"
    )

with col3:
    st.metric("Trip Days", trip_days)

st.success("Trip details captured successfully.")


import pandas as pd

# Initialize expense storage
if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.divider()

st.header("💳 Add Expense")

expense_name = st.text_input("Expense Name")

expense_amount = st.number_input(
    "Expense Amount",
    min_value=0.0,
    step=1.0
)

expense_currency = st.selectbox(
    "Currency",
    ["INR", "USD", "EUR", "JPY"]
)

expense_category = st.selectbox(
    "Category",
    [
        "Food",
        "Accommodation",
        "Transport",
        "Shopping",
        "Entertainment",
        "Miscellaneous"
    ]
)

if st.button("Add Expense"):

    if expense_name and expense_amount > 0:

        st.session_state.expenses.append(
            {
                "Expense": expense_name,
                "Amount": expense_amount,
                "Currency": expense_currency,
                "Category": expense_category
            }
        )

        st.success("Expense Added Successfully!")

    else:
        st.warning("Please enter valid expense details.")

st.divider()

# Dashboard Metrics

total_spent = sum(
    expense["Amount"]
    for expense in st.session_state.expenses
)

remaining_budget = budget - total_spent

transaction_count = len(
    st.session_state.expenses
)

st.header("📊 Budget Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Budget",
        f"₹{budget:,.0f}"
    )

with col2:
    st.metric(
        "Total Spent",
        f"₹{total_spent:,.0f}"
    )

with col3:
    st.metric(
        "Remaining Budget",
        f"₹{remaining_budget:,.0f}"
    )

with col4:
    st.metric(
        "Transactions",
        transaction_count
    )

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
    st.info("No expenses added yet.")