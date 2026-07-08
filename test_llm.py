from services.llm_service import LLMService


llm = LLMService()


print("\n----- Finance JSON Test -----")

finance_response = llm.generate_response(
    system_prompt="""
You are a travel finance assistant.
Return only valid JSON.
""",

    user_prompt="""
A traveler spent:

Flight: 500 USD
Hotel: 300 USD
Food: 100 USD

Create an expense summary.

Return this format:

{
    "total_expense_usd": number,
    "categories": {
        "flight": number,
        "hotel": number,
        "food": number
    },
    "advice": string
}
""",

    return_json=True
)

print(finance_response)