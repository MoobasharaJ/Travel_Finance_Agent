from agent.forex_agent import ForexAgent


agent = ForexAgent()


result = agent.analyze_forex(
    destination="Japan",
    budget=50000
)


print(result)