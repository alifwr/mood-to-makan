from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.services.s3_service import s3_service
from app.api import deps
from app.models.food import Food
from app.models.store import Store
from app.schemas.food import (
    FoodCreate, 
    FoodUpdate, 
    FoodResponse
)
from app.services.ai_service import generate_food_embedding
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=FoodResponse, status_code=201)
def create_food(
    *,
    db: Session = Depends(deps.get_db),
    food_in: FoodCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    
    # Allowed roles
    if current_user.role not in ["admin", "umkm", "client"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Check duplicate food name
    duplicate = db.query(Food).filter(Food.name == food_in.name, ((Food.store_id == food_in.store_id) | (Food.store_id == None))).first()
    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Food name already exists in this store or global list"
        )
    
    # is_valid_food
    is_valid = current_user.role in ["admin", "umkm"]

    # Generate embedding
    food_dict = food_in.model_dump()
    embedding = generate_food_embedding(food_dict)

    food = Food(
        **food_dict,
        embedding=embedding,
        is_valid_food=is_valid,
        user_id=current_user.id
    )

    db.add(food)
    db.commit()
    db.refresh(food)
    return food

@router.get("/", response_model=List[FoodResponse])
def list_foods(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    store_id: Optional[int] = Query(None, description="Filter by store_id"),
) -> Any:
    """
    Get list of foods with optional filters.
    """
    query = db.query(Food)
    
    if category:
        query = query.filter(Food.category == category)

    if store_id:
        query = query.filter(Food.store_id == store_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Food.name.ilike(search_pattern)) | 
            (Food.description.ilike(search_pattern))
        )
    
    foods = query.offset(skip).limit(limit).all()
    return foods


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get specific food by ID.
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.put("/{food_id}", response_model=FoodResponse)
def update_food(
    *,
    db: Session = Depends(deps.get_db),
    food_id: int,
    food_in: FoodUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:

    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if food.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = food_in.model_dump(exclude_unset=True)

    # ====== DUPLICATE CHECK FOR UPDATE ======
    if "name" in update_data:
        new_name = update_data["name"]

        duplicate = (
            db.query(Food)
            .filter(
                Food.id != food_id,  
                Food.name == new_name,
                ((Food.store_id == food.store_id) | (Food.store_id == None))
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Food name already exists in this store"
            )

    # Update fields normally
    for field, value in update_data.items():
        setattr(food, field, value)

    # Check if need regenerate embedding
    content_fields = ['name', 'description', 'main_ingredients',
                      'taste_profile', 'texture', 'mood_tags']
    needs_embedding_update = any(field in update_data for field in content_fields)

    if needs_embedding_update:
        food_dict = {
            'name': food.name,
            'description': food.description,
            'category': food.category,
            'main_ingredients': food.main_ingredients,
            'taste_profile': food.taste_profile,
            'texture': food.texture,
            'mood_tags': food.mood_tags
        }
        food.embedding = generate_food_embedding(food_dict)

    db.commit()
    db.refresh(food)
    return food

@router.put("/{food_id}/image", response_model=FoodResponse)
def upload_food_image(
    *,
    db: Session = Depends(deps.get_db),
    food_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Upload image for food item (UMKM only, or admin).
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if food.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Upload to S3
    image_url = s3_service.upload_file(file, folder="foods")

    # Update DB
    food.image_url = image_url
    db.add(food)
    db.commit()
    db.refresh(food)

    return food


@router.delete("/{food_id}", status_code=204)
def delete_food(
    *,
    db: Session = Depends(deps.get_db),
    food_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> None:
    """
    Delete food item.
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    if food.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(food)
    db.commit()
    
    return None

@router.put("/{food_id}/validate", response_model=FoodResponse)
def validate_food(
    *,
    db: Session = Depends(deps.get_db),
    food_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Mark a food item as valid (admin only).
    """
    # Check role
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can validate food")

    # Check food existence
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    # Mark as valid
    food.is_valid_food = True

    db.commit()
    db.refresh(food)
    return food

@router.put("/{food_id}/invalidate", response_model=FoodResponse)
def invalidate_food(
    *,
    db: Session = Depends(deps.get_db),
    food_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Mark a food item as invalid (admin only).
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can invalidate food")

    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    food.is_valid_food = False

    db.commit()
    db.refresh(food)
    return food
