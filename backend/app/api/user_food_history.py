from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.user_food_history import UserFoodHistory
from app.models.food import Food
from app.schemas.user_food_history import (
    UserFoodHistoryCreate,
    UserFoodHistoryResponse,
    UserFoodPreferences
)

router = APIRouter()

@router.get("/me/food-history", response_model=List[UserFoodHistoryResponse])
def get_user_food_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 50,
) -> Any:
    history = (
        db.query(UserFoodHistory)
        .filter(UserFoodHistory.user_id == current_user.id)
        .order_by(UserFoodHistory.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return history


@router.post("/me/food-history", response_model=UserFoodHistoryResponse, status_code=201)
def create_food_history(
    history_in: UserFoodHistoryCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    food = db.query(Food).filter(Food.id == history_in.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    history = UserFoodHistory(
        user_id=current_user.id,
        **history_in.model_dump()
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.get("/me/food-preferences", response_model=UserFoodPreferences)
def get_user_food_preferences(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:

    history = (
        db.query(UserFoodHistory)
        .filter(UserFoodHistory.user_id == current_user.id)
        .all()
    )

    if not history:
        return UserFoodPreferences(
            favorite_categories=[],
            favorite_tastes=[],
            favorite_moods=[],
            average_rating=None,
            total_interactions=0,
            most_selected_foods=[]
        )

    food_ids = [h.food_id for h in history]
    foods = db.query(Food).filter(Food.id.in_(food_ids)).all()
    food_map = {f.id: f for f in foods}

    categories, tastes, moods, ratings = [], [], [], []
    food_selection_count = {}

    for h in history:
        food = food_map.get(h.food_id)
        if not food:
            continue

        if food.category:
            categories.append(food.category)

        if food.taste_profile:
            tastes.extend(food.taste_profile)

        if food.mood_tags:
            moods.extend(food.mood_tags)

        if h.interaction_type == "rated" and h.rating is not None:
            ratings.append(h.rating)

        if h.interaction_type == "selected":
            food_selection_count[h.food_id] = food_selection_count.get(h.food_id, 0) + 1

    from collections import Counter

    favorite_categories = [c for c, _ in Counter(categories).most_common(3)]
    favorite_tastes = [t for t, _ in Counter(tastes).most_common(5)]
    favorite_moods = [m for m, _ in Counter(moods).most_common(5)]

    most_selected_foods = [
        {
            "food_id": food_id,
            "food_name": food_map[food_id].name,
            "selection_count": count,
        }
        for food_id, count in sorted(
            food_selection_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        if food_id in food_map
    ]

    avg_rating = sum(ratings) / len(ratings) if ratings else None

    return UserFoodPreferences(
        favorite_categories=favorite_categories,
        favorite_tastes=favorite_tastes,
        favorite_moods=favorite_moods,
        average_rating=avg_rating,
        total_interactions=len(history),
        most_selected_foods=most_selected_foods
    )
