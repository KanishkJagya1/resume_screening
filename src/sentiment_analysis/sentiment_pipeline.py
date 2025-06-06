# src/sentiment_analysis/sentiment_pipeline.py
import pandas as pd
from .data_processor import SentimentDataProcessor
from .llm_sentiment_analyzer import LLMSentimentAnalyzer

class SentimentAnalysisPipeline:
    def __init__(self):
        self.data_processor = SentimentDataProcessor()
        self.llm_analyzer = LLMSentimentAnalyzer()
    
    def load_feedback_data(self, file_path: str) -> pd.DataFrame:
        """Load employee feedback data"""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def run_sentiment_analysis(self, feedback_df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """Run complete sentiment analysis pipeline"""
        print("Step 1: Processing feedback data...")
        processed_df = self.data_processor.process_feedback_data(feedback_df, text_column)
        
        print("Step 2: Running LLM sentiment analysis...")
        feedback_texts = processed_df['processed_text'].tolist()
        llm_results = self.llm_analyzer.batch_analyze_sentiments(feedback_texts)
        
        print("Step 3: Combining results...")
        # Flatten LLM results into DataFrame columns
        for i, result in enumerate(llm_results):
            if 'error' not in result:
                processed_df.loc[i, 'llm_sentiment_score'] = result.get('sentiment_score', 0)
                processed_df.loc[i, 'llm_sentiment_label'] = result.get('sentiment_label', 'NEUTRAL')
                processed_df.loc[i, 'attrition_risk_level'] = result.get('attrition_risk', {}).get('risk_level', 'LOW')
                processed_df.loc[i, 'attrition_risk_score'] = result.get('attrition_risk', {}).get('risk_score', 0)
                processed_df.loc[i, 'engagement_level'] = result.get('engagement_level', {}).get('level', 'MEDIUM')
                processed_df.loc[i, 'key_themes'] = str(result.get('key_themes', []))
        
        return processed_df
    
    def generate_attrition_predictions(self, sentiment_df: pd.DataFrame) -> pd.DataFrame:
        """Generate attrition predictions for employees"""
        # Group by employee if employee_id column exists
        if 'employee_id' in sentiment_df.columns:
            employee_summaries = sentiment_df.groupby('employee_id').agg({
                'llm_sentiment_score': 'mean',
                'attrition_risk_score': 'mean',
                'engagement_level': lambda x: x.mode().iloc[0] if not x.empty else 'MEDIUM',
                'key_themes': lambda x: ', '.join(x.astype(str))
            }).reset_index()
            
            predictions = []
            for _, employee in employee_summaries.iterrows():
                employee_data = {
                    'avg_sentiment': employee['llm_sentiment_score'],
                    'engagement_level': employee['engagement_level'],
                    'recent_themes': employee['key_themes'].split(', ')
                }
                
                prediction = self.llm_analyzer.predict_attrition(employee_data)
                prediction['employee_id'] = employee['employee_id']
                predictions.append(prediction)
            
            return pd.DataFrame(predictions)
        else:
            return pd.DataFrame()