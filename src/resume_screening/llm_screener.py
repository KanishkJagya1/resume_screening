# src/resume_screening/llm_screener.py
from config.google_ai_config import GoogleAIConfig
import json

class LLMResumeScreener:
    def __init__(self):
        self.ai_config = GoogleAIConfig()
        self.model = self.ai_config.get_model()
    
    def create_screening_prompt(self, resume_text: str, job_requirements: dict) -> str:
        """Create optimized prompt for resume screening"""
        prompt = f"""
        You are an expert HR recruiter. Analyze the following resume against the job requirements and provide a detailed evaluation.

        JOB REQUIREMENTS:
        - Required Skills: {', '.join(job_requirements.get('skills', []))}
        - Experience Required: {job_requirements.get('experience_years', 0)} years
        - Education: {', '.join(job_requirements.get('education', []))}

        RESUME TEXT:
        {resume_text}

        Please provide your analysis in the following JSON format:
        {{
            "overall_score": <score out of 100>,
            "skills_match": {{
                "matched_skills": [list of matched skills],
                "missing_skills": [list of missing critical skills],
                "skills_score": <score out of 100>
            }},
            "experience_match": {{
                "candidate_experience": <years>,
                "meets_requirement": <true/false>,
                "experience_score": <score out of 100>
            }},
            "education_match": {{
                "candidate_education": [list],
                "meets_requirement": <true/false>,
                "education_score": <score out of 100>
            }},
            "strengths": [list of candidate strengths],
            "concerns": [list of potential concerns],
            "recommendation": "HIRE/CONSIDER/REJECT"
        }}
        
        Be objective and thorough in your analysis.
        """
        return prompt
    
    def screen_resume(self, resume_text: str, job_requirements: dict) -> dict:
        """Screen resume using Google AI"""
        prompt = self.create_screening_prompt(resume_text, job_requirements)
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            # Find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"Error in resume screening: {e}")
            return {
                "overall_score": 0,
                "error": str(e)
            }
    
    def batch_screen_resumes(self, resumes_data: list, job_requirements: dict) -> list:
        """Screen multiple resumes"""
        results = []
        for i, resume_data in enumerate(resumes_data):
            print(f"Screening resume {i+1}/{len(resumes_data)}")
            result = self.screen_resume(resume_data['text'], job_requirements)
            result['resume_id'] = resume_data.get('id', i)
            result['candidate_email'] = resume_data.get('email', '')
            results.append(result)
        
        return results