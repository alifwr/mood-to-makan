from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ClientBadge(Base):
    __tablename__ = "client_badges"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badges = Column(JSON, default=[], nullable=False)  # List of badge objects
    reviewed_stores_id = Column(JSON, default=[], nullable=False)  # List of reviewed store IDs

    # Relationships
    client = relationship("User", back_populates="client_badges")
