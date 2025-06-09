import os
import google.generativeai as genai
from dotenv import load_dotenv


class GoogleAIConfig:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)

    def get_model(self):
        return genai.GenerativeModel(model_name="gemini-1.5-pro")
