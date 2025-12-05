from typing import Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services import ai_service
from app.schemas.food import FoodSearchRequest, FoodRecommendationResponse, FoodRecommendationItem
from app.schemas.description import (
    DescriptionGenerateRequest,
    DescriptionEnhanceRequest,
    DescriptionResponse,
    EnhancedDescriptionResponse,
    PromotionalKeywordsResponse,
    FlavorCharacteristics
)

router = APIRouter()

@router.post("/search")
def search(
    query: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    results = ai_service.search_stores_by_vector(query, db)
    return results

@router.post("/recommend")
def recommend(
    preferences: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    recommendation = ai_service.recommend_food(preferences, db)
    return {"recommendation": recommendation}


# ========== FOOD RECOMMENDATION ENDPOINTS ==========

@router.post("/recommend-food", response_model=FoodRecommendationResponse)
def recommend_food(
    request: FoodSearchRequest,
    db: Session = Depends(deps.get_db),
    current_user: Optional[Any] = Depends(deps.get_current_user_optional),
) -> Any:
    """
    Get AI-powered food recommendations based on mood/preferences.
    Uses vector similarity and LLM for personalized suggestions.
    """
    user_id = current_user.id if current_user else None
    
    result = ai_service.recommend_foods_by_mood(
        mood_description=request.query,
        db=db,
        user_id=user_id,
        limit=request.limit
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
        query=request.query,
        total_results=len(recommendations)
    )


@router.post("/search-food")
def search_food(
    request: FoodSearchRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Search foods using semantic vector search.
    Supports filtering by category, calories, and ingredients.
    """
    try:
        foods = ai_service.search_foods_by_vector(
            query=request.query,
            db=db,
            limit=request.limit,
            category=request.category,
            max_calories=request.max_calories
        )
        
        # Convert SQLAlchemy models to dicts for serialization
        from app.schemas.food import FoodResponse
        foods_data = [FoodResponse.model_validate(food) for food in foods]
        
        return {
            "foods": foods_data,
            "query": request.query,
            "total_results": len(foods_data)
        }
    except Exception as e:
        import traceback
        print(f"Error in search_food: {e}")
        traceback.print_exc()
        return {
            "foods": [],
            "query": request.query,
            "total_results": 0,
            "error": str(e)
        }


@router.get("/personalized-recommendations")
def get_personalized_recommendations(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
    limit: int = 10,
) -> Any:
    """
    Get personalized food recommendations based on user's interaction history.
    Requires authentication.
    """
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


# ========== DESCRIPTION GENERATION ENDPOINTS ==========

@router.post("/generate-description", response_model=DescriptionResponse)
def generate_description(
    request: DescriptionGenerateRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Generate compelling food descriptions using AI.
    Returns short description, long description, selling points, and flavor characteristics.
    """
    result = ai_service.generate_food_description(
        name=request.name,
        category=request.category,
        main_ingredients=request.main_ingredients,
        taste_profile=request.taste_profile,
        texture=request.texture,
        region=request.region,
        selling_points=request.selling_points,
        style=request.style,
        language=request.language,
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


@router.post("/enhance-description", response_model=EnhancedDescriptionResponse)
def enhance_description(
    request: DescriptionEnhanceRequest,
) -> Any:
    """
    Enhance an existing food description using AI.
    """
    enhanced = ai_service.enhance_food_description(
        current_description=request.current_description,
        food_name=request.food_name,
        category=request.category,
        enhance_for=request.enhance_for,
        additional_info=request.additional_info
    )
    
    return EnhancedDescriptionResponse(enhanced_description=enhanced)


@router.get("/promotional-keywords", response_model=PromotionalKeywordsResponse)
def get_promotional_keywords(
    category: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get promotional keywords for a specific food category.
    """
    try:
        keywords = ai_service.get_promotional_keywords_for_category(category, db)
        return PromotionalKeywordsResponse(category=category, **keywords)
    except Exception as e:
        print(f"Error getting promotional keywords: {e}")
        # Return empty keywords if there's an error
        return PromotionalKeywordsResponse(
            category=category,
            selling_points=[],
            flavors=[],
            textures=[],
            moods=[],
            general=[]
        )
