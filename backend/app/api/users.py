from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, UserUpdate
from app.services.s3_service import s3_service

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:

    # Validate password
    if user_in.password is not None:
        if user_in.password.strip() == "":
            raise HTTPException(status_code=400, detail="Password cannot be empty")
        current_user.hashed_password = security.get_password_hash(user_in.password)

    # Validate full_name
    if user_in.full_name is not None:
        if user_in.full_name.strip() == "":
            raise HTTPException(status_code=400, detail="Full name cannot be empty")
        current_user.full_name = user_in.full_name

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/image", response_model=UserSchema)
def upload_user_image(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
) -> Any:

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image (jpg/png)"
        )

    try:
        image_url = s3_service.upload_file(file, folder="users")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload image")

    current_user.image_url = image_url
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

