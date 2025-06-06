# config/google_ai_config.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleAIConfig:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_model(self):
        return self.model