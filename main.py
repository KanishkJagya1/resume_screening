import streamlit as st
import pandas as pd
import os
from src.resume_screening.screening_pipeline import ResumeScreeningPipeline
from src.sentiment_analysis.sentiment_pipeline import SentimentAnalysisPipeline

def main():
    st.title("HR-Tech Innovation Challenge")
    st.sidebar.title("Navigation")
    
    app_mode = st.sidebar.selectbox("Choose Module", 
        ["Resume Screening", "Sentiment Analysis"])
    
    if app_mode == "Resume Screening":
        resume_screening_app()
    elif app_mode == "Sentiment Analysis":
        sentiment_analysis_app()

def resume_screening_app():
    st.header("Resume Screening System")
    
    # Job description input
    job_desc = st.text_area("Enter Job Description:", height=200)
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload Resumes", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )
    
    if st.button("Screen Resumes") and job_desc and uploaded_files:
        # Save uploaded files temporarily
        os.makedirs("temp_resumes", exist_ok=True)
        for uploaded_file in uploaded_files:
            with open(f"temp_resumes/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        # Run screening
        pipeline = ResumeScreeningPipeline()
        results = pipeline.run_screening("temp_resumes", job_desc)
        
        # Display results
        st.subheader("Screening Results")
        st.dataframe(results[['filename', 'overall_score', 'recommendation']])
        
        # Download results
        csv = results.to_csv(index=False)
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )
        
        # Clean up temporary files
        import shutil
        shutil.rmtree("temp_resumes")

def sentiment_analysis_app():
    st.header("Employee Sentiment Analysis")
    
    # File upload for feedback data
    uploaded_file = st.file_uploader(
        "Upload Employee Feedback Data (CSV/Excel)", 
        type=['csv', 'xlsx']
    )
    
    if uploaded_file:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Select text column
        text_columns = df.select_dtypes(include=['object']).columns.tolist()
        selected_column = st.selectbox("Select Feedback Text Column:", text_columns)
        
        if st.button("Analyze Sentiment") and selected_column:
            pipeline = SentimentAnalysisPipeline()
            
            with st.spinner("Analyzing sentiment..."):
                results = pipeline.run_sentiment_analysis(df, selected_column)
                
                # Display results
                st.subheader("Sentiment Analysis Results")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_sentiment = results['llm_sentiment_score'].mean()
                    st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
                
                with col2:
                    positive_pct = (results['llm_sentiment_label'] == 'POSITIVE').mean() * 100
                    st.metric("Positive Feedback", f"{positive_pct:.1f}%")
                
                with col3:
                    high_risk_pct = (results['attrition_risk_level'] == 'HIGH').mean() * 100
                    st.metric("High Attrition Risk", f"{high_risk_pct:.1f}%")
                
                with col4:
                    low_engagement_pct = (results['engagement_level'] == 'LOW').mean() * 100
                    st.metric("Low Engagement", f"{low_engagement_pct:.1f}%")
                
                # Detailed results
                st.subheader("Detailed Results")
                display_columns = [
                    'llm_sentiment_score', 'llm_sentiment_label', 
                    'attrition_risk_level', 'engagement_level', 'key_themes'
                ]
                st.dataframe(results[display_columns])
                
                # Attrition predictions
                if 'employee_id' in df.columns:
                    st.subheader("Attrition Risk Predictions")
                    predictions = pipeline.generate_attrition_predictions(results)
                    if not predictions.empty:
                        st.dataframe(predictions)
                
                # Download results
                csv = results.to_csv(index=False)
                st.download_button(
                    label="Download Sentiment Analysis Results",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
