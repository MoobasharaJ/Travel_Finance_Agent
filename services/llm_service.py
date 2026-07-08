"""
LLM Service

Handles:

- Gemini API communication
- Prompt execution
- Plain text generation
- JSON response generation
"""

import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class LLMService:
    """
    Wrapper around Gemini API.
    """

    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self):
        """
        Initialize Gemini client.
        """

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        return_json: bool = False
    ):
        """
        Generate response from Gemini.
        """

        full_prompt = f"""
{system_prompt}

{user_prompt}
"""

        config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1024
        )

        if return_json:
            config.response_mime_type = "application/json"

        # Retry once if JSON parsing fails
        for attempt in range(2):

            try:

                response = self.client.models.generate_content(
                    model=self.MODEL_NAME,
                    contents=full_prompt,
                    config=config
                )

                text = response.text.strip()

                if not return_json:
                    return text

                return json.loads(text)

            except json.JSONDecodeError:

                if attempt == 0:
                    continue

                return {
                    "success": False,
                    "error": "Invalid JSON returned by Gemini.",
                    "raw_response": text
                }

            except Exception as e:

                return {
                    "success": False,
                    "error": str(e)
                }