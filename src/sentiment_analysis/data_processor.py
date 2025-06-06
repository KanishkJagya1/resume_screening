# src/sentiment_analysis/data_processor.py
import pandas as pd
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

class SentimentDataProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """Remove stopwords from text"""
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def process_feedback_data(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """Process employee feedback data"""
        df_processed = df.copy()
        
        # Clean text
        df_processed['cleaned_text'] = df_processed[text_column].apply(self.clean_text)
        df_processed['processed_text'] = df_processed['cleaned_text'].apply(self.remove_stopwords)
        
        # Basic sentiment analysis using TextBlob
        df_processed['textblob_sentiment'] = df_processed['cleaned_text'].apply(
            lambda x: TextBlob(x).sentiment.polarity
        )
        df_processed['textblob_subjectivity'] = df_processed['cleaned_text'].apply(
            lambda x: TextBlob(x).sentiment.subjectivity
        )
        
        return df_processed