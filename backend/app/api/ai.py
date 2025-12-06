from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.services import ai_service
from app.models.food import Food
from app.models.user import User
from app.schemas.store import Store as StoreSchema
from app.schemas.food import FoodRecommendationResponse, FoodRecommendationItem
from app.schemas.description import (
    DescriptionResponse,
    EnhancedDescriptionResponse,
    FlavorCharacteristics
)

router = APIRouter()

# ========== AI POWERED STORE RECOMMENDATION ENDPOINTS ==========

@router.get("/search-stores")
def search_stores(
    query: str,
    db: Session = Depends(deps.get_db),
) -> List[StoreSchema]:
    results = ai_service.search_stores_by_vector(query, db)
    # Convert SQLAlchemy models to Pydantic schemas
    return [StoreSchema.model_validate(store) for store in results]

@router.get("/recommend-stores")
def recommend_stores(
    preferences: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    recommendation = ai_service.recommend_food(preferences, db)
    return {"recommendation": recommendation}


# ========== AI POWERED FOOD RECOMMENDATION ENDPOINTS ==========

@router.get("/search-foods")
def search_foods(
    query: str,
    db: Session = Depends(deps.get_db),
    limit: int = 5,
    category: Optional[str] = None,
    max_calories: Optional[float] = None,
) -> Any:
    try:
        foods = ai_service.search_foods_by_vector(
            query=query,
            db=db,
            limit=limit,
            category=category,
            max_calories=max_calories
        )
        
        from app.schemas.food import FoodResponse
        foods_data = [FoodResponse.model_validate(food) for food in foods]
        
        return {
            "foods": foods_data,
            "query": query,
            "total_results": len(foods_data)
        }
    except Exception as e:
        import traceback
        print(f"Error in search_food: {e}")
        traceback.print_exc()
        return {
            "foods": [],
            "query": query,
            "total_results": 0,
            "error": str(e)
        }

@router.get("/recommend-foods", response_model=FoodRecommendationResponse)
def recommend_foods(
    query: str,
    db: Session = Depends(deps.get_db),
    current_user: Optional[Any] = Depends(deps.get_current_user_optional),
    limit: int = 10,
) -> Any:
    user_id = current_user.id if current_user else None
    
    result = ai_service.recommend_foods_by_mood(
        mood_description=query,
        db=db,
        user_id=user_id,
        limit=limit
    )
    
    # Build response
    recommendations = [
        FoodRecommendationItem(
            food=food,
            similarity_score=None,  # Could calculate if needed
            reason=None
        )
        for food in result["recommendations"]
    ]
    
    return FoodRecommendationResponse(
        recommendations=recommendations,
        query=query,
        total_results=len(recommendations)
    )

@router.get("/personalized-recommendations")
def personalized_recommendations(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
    limit: int = 10,
) -> Any:
    try:
        foods = ai_service.get_personalized_recommendations(
            user_id=current_user.id,
            db=db,
            limit=limit
        )
        
        # Convert SQLAlchemy models to dicts for serialization
        from app.schemas.food import FoodResponse
        foods_data = [FoodResponse.model_validate(food) for food in foods]
        
        return {
            "recommendations": foods_data,
            "total_results": len(foods_data)
        }
    except Exception as e:
        import traceback
        print(f"Error in get_personalized_recommendations: {e}")
        traceback.print_exc()
        return {
            "recommendations": [],
            "total_results": 0,
            "error": str(e)
        }


# ========== FOOD DESCRIPTION GENERATION ENDPOINTS ==========

@router.post("/generate-food-description/{food_id}", response_model=DescriptionResponse)
def generate_food_description(
    food_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Generate compelling food descriptions using AI based on existing food data.
    Only the owner of the food can use this endpoint.
    Returns short description, long description, selling points, and flavor characteristics.
    """
    # Check if food exists
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    # Verify ownership
    if food.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to generate descriptions for this food"
        )
    
    # Use existing food data to generate description
    result = ai_service.generate_food_description(
        name=food.name,
        category=food.category,
        main_ingredients=food.main_ingredients or [],
        taste_profile=food.taste_profile or [],
        texture=food.texture or [],
        region=None,  # Could be added to food model if needed
        selling_points=None,
        style="promotional",
        language="en",
        db=db
    )
    
    # Convert flavor_characteristics dict to FlavorCharacteristics model if present
    if result.get("flavor_characteristics"):
        flavor_data = result["flavor_characteristics"]
        result["flavor_characteristics"] = FlavorCharacteristics(
            primary_flavors=flavor_data.get("primary_flavors", []),
            secondary_flavors=flavor_data.get("secondary_flavors", []),
            texture_description=flavor_data.get("texture_description", ""),
            aroma_notes=flavor_data.get("aroma_notes", "")
        )
    
    return DescriptionResponse(**result)

@router.post("/generate-enhanced-food-description/{food_id}", response_model=EnhancedDescriptionResponse)
def enhance_food_description(
    food_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Enhance an existing food description using AI based on current description.
    Only the owner of the food can use this endpoint.
    Automatically saves the enhanced description to the database.
    """
    # Check if food exists
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    # Verify ownership
    if food.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to enhance descriptions for this food"
        )
    
    # Use existing food description to enhance
    current_description = food.description or f"{food.name} - {food.category}"
    
    enhanced = ai_service.enhance_food_description(
        current_description=current_description,
        food_name=food.name,
        category=food.category,
        enhance_for="promotional",
        additional_info=None
    )
    
    # Save enhanced description to database
    food.enhanced_description = enhanced
    db.commit()
    db.refresh(food)
    
    return EnhancedDescriptionResponse(enhanced_description=enhanced)

