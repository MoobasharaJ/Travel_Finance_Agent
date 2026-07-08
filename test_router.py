from agent.router import TravelFinanceRouter
import pandas as pd


# Sample expense data
category_summary = pd.DataFrame({
    "Category": [
        "Hotel",
        "Food",
        "Transport"
    ],
    "Amount": [
        30000,
        10000,
        5000
    ]
})


router = TravelFinanceRouter()


result = router.generate_report(
    user_query="Analyze my complete trip.",

    destination="Japan",

    cost_level="Medium",

    budget=100000,

    total_spent=45000,

    trip_progress_percent=50,

    projected_total_spend=85000,

    category_summary=category_summary,

    highest_spending_category="Hotel",

    transaction_count=25
)


print(result)