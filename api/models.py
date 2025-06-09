# api/models.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class AnalysisType(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"

# Base Response Models
class APIResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[Dict[str, Any]] = None

# Resume Screening Models
class JobDescription(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    required_skills: List[str] = Field(..., min_items=1, max_items=50)
    preferred_skills: Optional[List[str]] = Field(default=[], max_items=30)
    experience_years: Optional[int] = Field(default=0, ge=0, le=50)
    education_level: Optional[str] = Field(default="", max_length=100)
    location: Optional[str] = Field(default="", max_length=100)
    
    @validator('required_skills', 'preferred_skills')
    def validate_skills(cls, v):
        if v:
            return [skill.strip() for skill in v if skill.strip()]
        return v

class ResumeText(BaseModel):
    content: str = Field(..., min_length=50, max_length=10000)
    filename: Optional[str] = Field(default="", max_length=255)

class ScreeningCriteria(BaseModel):
    skills_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    experience_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    education_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    keywords_weight: float = Field(default=0.1, ge=0.0, le=1.0)
    minimum_score: float = Field(default=0.5, ge=0.0, le=1.0)
    
    @validator('skills_weight', 'experience_weight', 'education_weight', 'keywords_weight')
    def validate_weights_sum(cls, v, values):
        weights = [v]
        for field in ['skills_weight', 'experience_weight', 'education_weight']:
            if field in values:
                weights.append(values[field])
        if len(weights) == 4 and sum(weights) != 1.0:
            raise ValueError('All weights must sum to 1.0')
        return v

class ResumeScreeningRequest(BaseModel):
    job_description: JobDescription
    resumes: List[ResumeText] = Field(..., min_items=1, max_items=100)
    criteria: Optional[ScreeningCriteria] = Field(default_factory=ScreeningCriteria)
    include_analysis: bool = Field(default=True)

class CandidateScore(BaseModel):
    filename: str
    overall_score: float = Field(..., ge=0.0, le=1.0)
    skills_score: float = Field(..., ge=0.0, le=1.0)
    experience_score: float = Field(..., ge=0.0, le=1.0)
    education_score: float = Field(..., ge=0.0, le=1.0)
    keywords_score: float = Field(..., ge=0.0, le=1.0)
    matched_skills: List[str]
    missing_skills: List[str]
    analysis: Optional[str] = None
    recommendation: str

class ResumeScreeningResponse(BaseModel):
    job_id: str
    total_resumes: int
    qualified_candidates: int
    results: List[CandidateScore]
    summary: Dict[str, Any]
    processing_time: float

# Sentiment Analysis Models
class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    source: Optional[str] = Field(default="", max_length=100)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class SentimentAnalysisRequest(BaseModel):
    texts: List[TextInput] = Field(..., min_items=1, max_items=1000)
    analysis_type: AnalysisType = Field(default=AnalysisType.BASIC)
    categories: Optional[List[str]] = Field(default=[], max_items=20)
    include_themes: bool = Field(default=False)
    include_emotions: bool = Field(default=False)

class SentimentResult(BaseModel):
    text: str
    sentiment: SentimentType
    confidence: float = Field(..., ge=0.0, le=1.0)
    positive_score: float = Field(..., ge=0.0, le=1.0)
    negative_score: float = Field(..., ge=0.0, le=1.0)
    neutral_score: float = Field(..., ge=0.0, le=1.0)
    themes: Optional[List[str]] = None
    emotions: Optional[Dict[str, float]] = None
    categories: Optional[Dict[str, float]] = None
    source: Optional[str] = None

class SentimentSummary(BaseModel):
    total_texts: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_confidence: float
    dominant_sentiment: SentimentType
    key_themes: List[str]
    sentiment_distribution: Dict[str, float]

class SentimentAnalysisResponse(BaseModel):
    analysis_id: str
    results: List[SentimentResult]
    summary: SentimentSummary
    processing_time: float
    analysis_type: AnalysisType

# File Upload Models
class FileUploadResponse(BaseModel):
    filename: str
    file_id: str
    size: int
    content_type: str
    status: str = "uploaded"

# Batch Processing Models
class BatchJobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class BatchJob(BaseModel):
    job_id: str
    job_type: str  # "resume_screening" or "sentiment_analysis"
    status: BatchJobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_items: int
    processed_items: int = 0
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    result_url: Optional[str] = None
    error_message: Optional[str] = None

class BatchJobRequest(BaseModel):
    job_type: str = Field(..., regex="^(resume_screening|sentiment_analysis)$")
    input_data: Dict[str, Any]
    callback_url: Optional[str] = None

# Health Check Models
class HealthStatus(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    uptime: float
    memory_usage: Dict[str, float]
    api_health: Dict[str, bool]

# Analytics Models
class UsageStats(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    requests_by_endpoint: Dict[str, int]
    requests_by_hour: Dict[str, int]

class APIMetrics(BaseModel):
    stats: UsageStats
    health: HealthStatus
    active_jobs: int
    queue_size: int