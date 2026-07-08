from agent.expense_agent import ExpenseAgent
import pandas as pd


# Sample category-wise expense data
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


# Create Expense Agent
agent = ExpenseAgent()


# Analyze expenses
result = agent.analyze_expenses(
    total_spent=45000,
    transaction_count=25,
    category_summary=category_summary,
    highest_spending_category="Hotel"
)


print(result)