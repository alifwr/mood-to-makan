from sqlalchemy import Integer, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import List

class ProblemCategory(Base):
    __tablename__ = "problem_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_key: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    keywords: Mapped[List[str]] = mapped_column(JSON, default=[], nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
