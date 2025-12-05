from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="client") # client, umkm, admin
    image_url = Column(String, nullable=True)
    
    # Relationships
    umkm_stores = relationship("Store", back_populates="umkm")
    foods = relationship("Food", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    client_badges = relationship("ClientBadge", back_populates="client")
    food_history = relationship("UserFoodHistory", back_populates="user")
