# src/resume_screening/resume_parser.py
import PyPDF2
import docx
import re
from typing import Dict, List

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'[\+]?[1-9]?[0-9]{7,14}'
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX resume"""
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume and extract key information"""
        if file_path.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        
        resume_data = {
            'text': text,
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text)
        }
        
        return resume_data
    
    def extract_email(self, text: str) -> str:
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text: str) -> str:
        phones = re.findall(self.phone_pattern, text)
        return phones[0] if phones else ""
    
    def extract_skills(self, text: str) -> List[str]:
        # Define skill keywords
        skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js',
            'django', 'flask', 'spring', 'mysql', 'postgresql', 'mongodb',
            'git', 'docker', 'kubernetes', 'aws', 'azure', 'jenkins'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def extract_experience(self, text: str) -> int:
        # Extract years of experience
        exp_patterns = [
            r'(\d+)[\s\-\+]*(?:years?|yrs?)[\s\-\+]*(?:of\s+)?(?:experience|exp)',
            r'(?:experience|exp)[\s\-\+]*(?:of\s+)?(\d+)[\s\-\+]*(?:years?|yrs?)'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return max(map(int, matches))
        
        return 0
    
    def extract_education(self, text: str) -> List[str]:
        edu_pattern = r'\b(bachelor|master|phd|b\.tech|m\.tech|bca|mca|be|me)\b'
        education = re.findall(edu_pattern, text.lower(), re.IGNORECASE)
        return list(set(education))