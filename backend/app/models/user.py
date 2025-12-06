import enum
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class UserRole(str, enum.Enum):
    client = "client"
    umkm = "umkm"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.client, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # Relationships
    umkm_stores = relationship("Store", back_populates="umkm")
    foods = relationship("Food", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    client_badges = relationship("ClientBadge", back_populates="client")
    food_history = relationship("UserFoodHistory", back_populates="user")
