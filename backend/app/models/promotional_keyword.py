from sqlalchemy import Integer, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import List

class PromotionalKeyword(Base):
    __tablename__ = "promotional_keywords"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False)
    keywords: Mapped[List[str]] = mapped_column(JSON, default=[], nullable=False)
    keyword_type: Mapped[str] = mapped_column(String, nullable=False) # selling_point, flavor, texture, mood, general
