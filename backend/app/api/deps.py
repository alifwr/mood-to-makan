from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        secret = settings.SECRET_KEY.get_secret_value() if settings.SECRET_KEY else "insecure-secret-key-dev-only"
        payload = jwt.decode(
            token, secret, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.email == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_user_optional(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme_optional)
) -> Optional[User]:
    """
    Optional authentication - returns user if token is valid, None otherwise.
    Does not raise exception if no token or invalid token.
    """
    if not token:
        return None
    
    try:
        secret = settings.SECRET_KEY.get_secret_value() if settings.SECRET_KEY else "insecure-secret-key-dev-only"
        payload = jwt.decode(
            token, secret, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
        user = db.query(User).filter(User.email == token_data.sub).first()
        return user
    except (JWTError, ValidationError):
        return None

