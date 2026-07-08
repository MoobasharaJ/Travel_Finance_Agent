from services.llm_service import LLMService

llm = LLMService()

response = llm.generate_response(
    "Explain why exchange rates fluctuate in 3 lines."
)

print(response)