from agent.budget_agent import BudgetAgent


agent = BudgetAgent()


result = agent.analyze_budget(
    destination="Japan",
    cost_level="Medium",
    budget=100000,
    total_spent=40000,
    trip_progress_percent=50,
    projected_total_spend=85000
)


print(result)