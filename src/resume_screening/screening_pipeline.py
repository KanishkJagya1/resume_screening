# src/resume_screening/screening_pipeline.py
import os
import pandas as pd
from .resume_parser import ResumeParser
from .job_parser import JobDescriptionParser
from .llm_screener import LLMResumeScreener

class ResumeScreeningPipeline:
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.job_parser = JobDescriptionParser()
        self.llm_screener = LLMResumeScreener()
    
    def process_resumes_folder(self, resumes_folder: str) -> list:
        """Process all resumes in a folder"""
        resumes_data = []
        
        for filename in os.listdir(resumes_folder):
            if filename.endswith(('.pdf', '.docx', '.txt')):
                file_path = os.path.join(resumes_folder, filename)
                try:
                    resume_data = self.resume_parser.parse_resume(file_path)
                    resume_data['filename'] = filename
                    resume_data['id'] = len(resumes_data)
                    resumes_data.append(resume_data)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return resumes_data
    
    def run_screening(self, resumes_folder: str, job_description: str) -> pd.DataFrame:
        """Run complete screening pipeline"""
        print("Step 1: Parsing job description...")
        job_requirements = self.job_parser.extract_requirements(job_description)
        
        print("Step 2: Processing resumes...")
        resumes_data = self.process_resumes_folder(resumes_folder)
        
        if not resumes_data:
            return pd.DataFrame()
        
        print("Step 3: Screening with LLM...")
        screening_results = self.llm_screener.batch_screen_resumes(resumes_data, job_requirements)
        
        print("Step 4: Compiling results...")
        # Combine resume data with screening results
        combined_results = []
        for i, (resume_data, screening_result) in enumerate(zip(resumes_data, screening_results)):
            combined_result = {
                'filename': resume_data.get('filename', f'resume_{i}'),
                'candidate_email': resume_data.get('email', ''),
                'candidate_phone': resume_data.get('phone', ''),
                'extracted_skills': ', '.join(resume_data.get('skills', [])),
                'extracted_experience': resume_data.get('experience', 0),
                'extracted_education': ', '.join(resume_data.get('education', [])),
                'overall_score': screening_result.get('overall_score', 0),
                'recommendation': screening_result.get('recommendation', 'REVIEW'),
                'skills_score': screening_result.get('skills_match', {}).get('skills_score', 0),
                'experience_score': screening_result.get('experience_match', {}).get('experience_score', 0),
                'education_score': screening_result.get('education_match', {}).get('education_score', 0),
                'matched_skills': ', '.join(screening_result.get('skills_match', {}).get('matched_skills', [])),
                'missing_skills': ', '.join(screening_result.get('skills_match', {}).get('missing_skills', [])),
                'strengths': ', '.join(screening_result.get('strengths', [])),
                'concerns': ', '.join(screening_result.get('concerns', [])),
                'error': screening_result.get('error', '')
            }
            combined_results.append(combined_result)
        
        df_results = pd.DataFrame(combined_results)
        df_results = df_results.sort_values('overall_score', ascending=False)
        
        return df_results
    
    def save_results(self, results_df: pd.DataFrame, output_path: str):
        """Save screening results"""
        results_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")