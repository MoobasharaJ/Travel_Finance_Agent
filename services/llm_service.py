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
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self):

        # First try local .env
        api_key = os.getenv("GEMINI_API_KEY")

        # If not found, try Streamlit Secrets
        if not api_key:
            api_key = st.secrets.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(api_key=api_key)

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