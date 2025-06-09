import json
import pandas as pd
from config.google_ai_config import GoogleAIConfig


class LLMSentimentAnalyzer:
    def __init__(self):
        try:
            self.ai_config = GoogleAIConfig()
            self.model = self.ai_config.get_model()
        except Exception as e:
            print(f"[ERROR] Failed to initialize GoogleAIConfig: {e}")
            self.model = None  # Gracefully fallback

    def create_sentiment_prompt(self, feedback_text: str) -> str:
        return f"""
        You are an expert HR analyst specializing in employee sentiment analysis. 
        Analyze the following employee feedback and provide a comprehensive assessment.

        EMPLOYEE FEEDBACK:
        "{feedback_text}"

        Please provide your analysis in the following JSON format:
        {{
            "sentiment_score": <score from -1 to 1>,
            "sentiment_label": "<POSITIVE/NEUTRAL/NEGATIVE>",
            "confidence": <0 to 1>,
            "key_themes": [themes],
            "emotional_indicators": [phrases],
            "attrition_risk": {{
                "risk_level": "<LOW/MEDIUM/HIGH>",
                "risk_score": <0 to 1>,
                "risk_factors": [factors]
            }},
            "engagement_level": {{
                "level": "<HIGH/MEDIUM/LOW>",
                "score": <0 to 1>,
                "positive_indicators": [signals],
                "negative_indicators": [signals]
            }},
            "actionable_insights": [recommendations]
        }}

        Focus on identifying subtle indicators of job satisfaction, engagement, and attrition risk.
        """

    def analyze_sentiment(self, feedback_text: str) -> dict:
        if not feedback_text.strip():
            return {"error": "Empty feedback text"}

        if not self.model:
            return {"error": "LLM model not initialized due to configuration error."}

        prompt = self.create_sentiment_prompt(feedback_text)

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            json_str = response_text[response_text.find('{'):response_text.rfind('}') + 1]
            return json.loads(json_str)
        except Exception as e:
            print(f"[ERROR] Sentiment analysis failed: {e}")
            return {"sentiment_score": 0, "error": str(e)}

    def batch_analyze_sentiments(self, feedback_list: list) -> list:
        results = []
        for i, feedback in enumerate(feedback_list):
            print(f"Analyzing feedback {i+1}/{len(feedback_list)}")
            results.append(self.analyze_sentiment(feedback))
        return results

    def create_attrition_prediction_prompt(self, employee_data: dict) -> str:
        return f"""
        You are an expert HR data scientist. Based on the employee data provided, 
        predict the likelihood of this employee leaving the company.

        EMPLOYEE DATA:
        - Recent Feedback Sentiment: {employee_data.get('avg_sentiment', 0)}
        - Engagement Level: {employee_data.get('engagement_level', 'Unknown')}
        - Tenure: {employee_data.get('tenure_months', 0)} months
        - Recent Feedback Count: {employee_data.get('feedback_count', 0)}
        - Department: {employee_data.get('department', 'Unknown')}
        - Role Level: {employee_data.get('role_level', 'Unknown')}
        RECENT FEEDBACK THEMES: {employee_data.get('recent_themes', [])}

        Respond in JSON:
        {{
            "attrition_probability": <0 to 1>,
            "risk_category": "<LOW/MEDIUM/HIGH>",
            "key_risk_factors": [factors],
            "protective_factors": [factors],
            "recommended_interventions": [actions],
            "priority_level": "<LOW/MEDIUM/HIGH/URGENT>",
            "confidence": <0 to 1>
        }}
        """

    def predict_attrition(self, employee_data: dict) -> dict:
        if not self.model:
            return {"error": "LLM model not initialized due to configuration error."}

        prompt = self.create_attrition_prediction_prompt(employee_data)

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            json_str = response_text[response_text.find('{'):response_text.rfind('}') + 1]
            return json.loads(json_str)
        except Exception as e:
            print(f"[ERROR] Attrition prediction failed: {e}")
            return {"attrition_probability": 0.5, "error": str(e)}
