from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.review import Review
from app.models.store import Store
from app.models.food import Food
from app.models.user import User
from app.schemas.review import ReviewCreate, Review as ReviewSchema
from app.schemas.review_analysis import (
    ReviewAnalysisRequest,
    ReviewAnalysisResponse,
    SentimentAnalysis,
    DetectedProblem,
    ProblemCategoryResponse
)
from app.services import ai_service

router = APIRouter()

@router.post("/", response_model=ReviewSchema)
def create_review(
    *,
    db: Session = Depends(deps.get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Validate that either store_id or food_id is provided
    if not review_in.store_id and not review_in.food_id:
        raise HTTPException(status_code=400, detail="Must provide store_id or food_id")
    
    if review_in.store_id:
        store = db.query(Store).filter(Store.id == review_in.store_id).first()
        if not store:
            raise HTTPException(status_code=404, detail="Store not found")
            
    if review_in.food_id:
        food = db.query(Food).filter(Food.id == review_in.food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food not found")

    review = Review(
        **review_in.model_dump(),
        user_id=current_user.id
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/store/{store_id}", response_model=List[ReviewSchema])
def read_reviews_by_store(
    store_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    reviews = db.query(Review).filter(Review.store_id == store_id).offset(skip).limit(limit).all()
    return reviews

@router.get("/food/{food_id}", response_model=List[ReviewSchema])
def read_reviews_by_food(
    food_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    reviews = db.query(Review).filter(Review.food_id == food_id).offset(skip).limit(limit).all()
    return reviews

@router.post("/analyze", response_model=ReviewAnalysisResponse)
def analyze_review(
    request: ReviewAnalysisRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Analyze a review for sentiment and detect problems.
    """
    # Analyze sentiment
    sentiment_result = ai_service.analyze_review_sentiment(request.text, request.rating)
    sentiment = SentimentAnalysis(**sentiment_result)
    
    # Detect problems
    problems_result = ai_service.categorize_review_problems(request.text, request.rating, db)
    detected_problems = [DetectedProblem(**p) for p in problems_result]
    
    # Extract topics
    topics = ai_service.extract_review_topics(request.text)
    
    return ReviewAnalysisResponse(
        sentiment=sentiment,
        detected_problems=detected_problems,
        topics=topics
    )

@router.get("/problem-categories", response_model=List[ProblemCategoryResponse])
def get_problem_categories(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get list of all problem categories for review analysis.
    """
    from app.models.problem_category import ProblemCategory
    
    try:
        categories = db.query(ProblemCategory).filter(ProblemCategory.is_active == True).all()
        return [
            ProblemCategoryResponse(
                category_key=cat.category_key,
                name=cat.name,
                description=cat.description,
                keywords=cat.keywords,
                is_active=cat.is_active
            )
            for cat in categories
        ]
    except Exception as e:
        # If problem_category table doesn't exist, return empty list
        print(f"Error fetching problem categories: {e}")
        return []

