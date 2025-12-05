from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.models.store import Store
from app.models.user import User
from app.schemas.store import StoreCreate, Store as StoreSchema, StoreUpdate
from app.services.s3_service import s3_service
from app.services.ai_service import generate_embedding

router = APIRouter()

@router.post("/", response_model=StoreSchema, status_code=201)
def create_store(
    *,
    db: Session = Depends(deps.get_db),
    store_in: StoreCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:

    # Allowed roles
    if current_user.role not in ["admin", "umkm", "client"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Check duplicate store name
    duplicate = db.query(Store).filter(Store.name == store_in.name).first()
    if duplicate:
        raise HTTPException(
            status_code=400,
            detail=f"Store with name '{store_in.name}' already exists"
        )

    # is_valid_store
    is_valid = current_user.role in ["admin", "umkm"]

    # Generate embedding
    embedding_text = f"{store_in.name} {store_in.description or ''} {store_in.address or ''}"
    embedding = generate_embedding(embedding_text)

    # Convert Pydantic → dict, remove umkm_id if provided by request
    store_data = store_in.model_dump(exclude={"umkm_id"})

    # Assign owner if UMKM
    if current_user.role == "umkm":
        store = Store(
            **store_data,
            umkm_id=current_user.id,
            embedding=embedding,
            is_valid_store=is_valid
        )
    else:
        # Admin & Client: no umkm_id attached
        store = Store(
            **store_data,
            embedding=embedding,
            is_valid_store=is_valid
        )

    db.add(store)
    db.commit()
    db.refresh(store)
    return store

@router.get("/", response_model=List[StoreSchema])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    stores = db.query(Store).offset(skip).limit(limit).all()
    return stores

@router.get("/{store_id}", response_model=StoreSchema)
def read_store(
    store_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@router.put("/{store_id}", response_model=StoreSchema)
def update_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    store_in: StoreUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.umkm_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = store_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(store, field, value)
    
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

@router.put("/{store_id}/image", response_model=StoreSchema)
def upload_store_image(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.umkm_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    image_url = s3_service.upload_file(file, folder="stores")
    store.image_url = image_url
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

@router.delete("/{store_id}", status_code=204)
def delete_store(
    *,
    db: Session = Depends(deps.get_db),
    store_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> None:
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.umkm_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
   
    db.delete(store)
    db.commit()
    return None

@router.put("/{store_id}/validate", response_model=StoreSchema)
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
    food = db.query(Store).filter(Store.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    # Mark as valid
    food.is_valid_food = True

    db.commit()
    db.refresh(food)
    return food

@router.put("/{store_id}/invalidate", response_model=StoreSchema)
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

    food = db.query(Store).filter(Store.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    food.is_valid_food = False

    db.commit()
    db.refresh(food)
    return food