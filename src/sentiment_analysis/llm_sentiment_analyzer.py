# src/sentiment_analysis/llm_sentiment_analyzer.py
from config.google_ai_config import GoogleAIConfig
import json
import pandas as pd

class LLMSentimentAnalyzer:
    def __init__(self):
        self.ai_config = GoogleAIConfig()
        self.model = self.ai_config.get_model()
    
    def create_sentiment_prompt(self, feedback_text: str) -> str:
        """Create optimized prompt for sentiment analysis"""
        prompt = f"""
        You are an expert HR analyst specializing in employee sentiment analysis. 
        Analyze the following employee feedback and provide a comprehensive assessment.

        EMPLOYEE FEEDBACK:
        "{feedback_text}"

        Please provide your analysis in the following JSON format:
        {{
            "sentiment_score": <score from -1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive>,
            "sentiment_label": "<POSITIVE/NEUTRAL/NEGATIVE>",
            "confidence": <confidence score from 0 to 1>,
            "key_themes": [list of main themes/topics mentioned],
            "emotional_indicators": [list of emotional words/phrases found],
            "attrition_risk": {{
                "risk_level": "<LOW/MEDIUM/HIGH>",
                "risk_score": <score from 0 to 1>,
                "risk_factors": [list of factors indicating potential attrition]
            }},
            "engagement_level": {{
                "level": "<HIGH/MEDIUM/LOW>",
                "score": <score from 0 to 1>,
                "positive_indicators": [list of positive engagement signals],
                "negative_indicators": [list of negative engagement signals]
            }},
            "actionable_insights": [list of specific recommendations for management]
        }}

        Focus on identifying subtle indicators of job satisfaction, engagement, and potential attrition risks.
        """
        return prompt
    
    def analyze_sentiment(self, feedback_text: str) -> dict:
        """Analyze sentiment using Google AI"""
        if not feedback_text or feedback_text.strip() == "":
            return {"error": "Empty feedback text"}
        
        prompt = self.create_sentiment_prompt(feedback_text)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                "sentiment_score": 0,
                "error": str(e)
            }
    
    def batch_analyze_sentiments(self, feedback_list: list) -> list:
        """Analyze multiple feedback entries"""
        results = []
        for i, feedback in enumerate(feedback_list):
            print(f"Analyzing feedback {i+1}/{len(feedback_list)}")
            result = self.analyze_sentiment(feedback)
            results.append(result)
        
        return results
    
    def create_attrition_prediction_prompt(self, employee_data: dict) -> str:
        """Create prompt for attrition prediction"""
        prompt = f"""
        You are an expert HR data scientist. Based on the employee data provided, 
        predict the likelihood of this employee leaving the company.

        EMPLOYEE DATA:
        - Recent Feedback Sentiment: {employee_data.get('avg_sentiment', 0)}
        - Engagement Level: {employee_data.get('engagement_level', 'Unknown')}
        - Tenure: {employee_data.get('tenure_months', 0)} months
        - Recent Feedback Count: {employee_data.get('feedback_count', 0)}
        - Department: {employee_data.get('department', 'Unknown')}
        - Role Level: {employee_data.get('role_level', 'Unknown')}

        RECENT FEEDBACK THEMES:
        {employee_data.get('recent_themes', [])}

        Please provide your prediction in JSON format:
        {{
            "attrition_probability": <probability from 0 to 1>,
            "risk_category": "<LOW/MEDIUM/HIGH>",
            "key_risk_factors": [list of main factors contributing to risk],
            "protective_factors": [list of factors reducing risk],
            "recommended_interventions": [specific actions to reduce attrition risk],
            "priority_level": "<LOW/MEDIUM/HIGH/URGENT>",
            "confidence": <confidence in prediction from 0 to 1>
        }}
        """
        return prompt
    
    def predict_attrition(self, employee_data: dict) -> dict:
        """Predict employee attrition risk"""
        prompt = self.create_attrition_prediction_prompt(employee_data)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"Error in attrition prediction: {e}")
            return {
                "attrition_probability": 0.5,
                "error": str(e)
            }