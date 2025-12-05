from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ReviewAnalysisRequest(BaseModel):
    text: str = Field(..., description="Review text to analyze")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class SentimentAnalysis(BaseModel):
    score: float = Field(..., description="Sentiment score from -1.0 to 1.0")
    label: str = Field(..., description="Sentiment label: positive, neutral, or negative")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")
    reasoning: Optional[str] = Field(None, description="Explanation of the sentiment")


class DetectedProblem(BaseModel):
    category: str = Field(..., description="Problem category key")
    category_name: Optional[str] = Field(None, description="Human readable category name")
    severity: float = Field(..., ge=0.0, le=1.0, description="Problem severity")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    evidence: Optional[str] = Field(None, description="Evidence text from review")


class ReviewAnalysisResponse(BaseModel):
    sentiment: SentimentAnalysis
    detected_problems: List[DetectedProblem]
    topics: Optional[List[str]] = Field(None, description="Key topics extracted from review")


class ProblemCategoryResponse(BaseModel):
    category_key: str
    name: str
    description: str
    keywords: List[str]
    is_active: bool
