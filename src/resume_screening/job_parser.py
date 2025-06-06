# src/resume_screening/job_parser.py
import re
from typing import Dict, List

class JobDescriptionParser:
    def __init__(self):
        self.skill_patterns = {
            'programming': r'\b(python|java|javascript|c\+\+|react|angular|node\.js)\b',
            'databases': r'\b(mysql|postgresql|mongodb|redis|oracle)\b',
            'frameworks': r'\b(django|flask|spring|express|laravel)\b',
            'tools': r'\b(git|docker|kubernetes|jenkins|aws|azure)\b'
        }
    
    def extract_requirements(self, job_description: str) -> Dict:
        """Extract key requirements from job description"""
        requirements = {
            'skills': [],
            'experience_years': 0,
            'education': [],
            'certifications': []
        }
        
        # Extract skills
        text_lower = job_description.lower()
        for category, pattern in self.skill_patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            requirements['skills'].extend(matches)
        
        # Extract experience years
        exp_pattern = r'(\d+)[\s\-\+]*(?:years?|yrs?)'
        exp_matches = re.findall(exp_pattern, text_lower)
        if exp_matches:
            requirements['experience_years'] = max(map(int, exp_matches))
        
        # Extract education requirements
        edu_pattern = r'\b(bachelor|master|phd|b\.tech|m\.tech|bca|mca)\b'
        edu_matches = re.findall(edu_pattern, text_lower, re.IGNORECASE)
        requirements['education'] = list(set(edu_matches))
        
        return requirements

# Usage example
job_parser = JobDescriptionParser()
job_desc = """
We are looking for a Software Engineer with 3+ years of experience.
Required skills: Python, Django, PostgreSQL, Docker, AWS.
Education: Bachelor's degree in Computer Science or related field.
"""
job_requirements = job_parser.extract_requirements(job_desc)
print(job_requirements)