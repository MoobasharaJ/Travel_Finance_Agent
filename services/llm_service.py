"""
LLM Service

Responsible for:
- Loading Gemini API
- Sending prompts
- Returning AI responses

No calculations.
No database.
No prompt creation.
"""

import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file."
            )

        self.client = genai.Client(api_key=api_key)

        # Centralized model name
        self.model = "gemini-2.5-flash"

    # =====================================================
    # Generate Response
    # =====================================================

    def generate_response(self, prompt):
        """
        Send prompt to Gemini and return plain text response.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:

            return f"LLM Error: {str(e)}"