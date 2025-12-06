from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.review import Review
from app.models.store import Store
from app.models.food import Food
from app.models.user import User
from app.schemas.review import ReviewCreate, Review as ReviewSchema
from app.services.ai_service import generate_embedding

router = APIRouter()

@router.post("/", response_model=ReviewSchema, status_code=201)
def create_review(
    *,
    db: Session = Depends(deps.get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:

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

    embedding = generate_embedding(review_in.comment)

    review = Review(
        user_id=current_user.id,
        rating=review_in.rating,
        comment=review_in.comment,
        store_id=review_in.store_id,
        food_id=review_in.food_id,
        embedding=embedding
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
