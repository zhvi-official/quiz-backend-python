import uuid
import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String, Text, Integer, Boolean, DateTime, ForeignKey, Index, 
    UniqueConstraint, Enum, func, Uuid, ForeignKeyConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    quizzes: Mapped[List["Quiz"]] = relationship(
        secondary="quiz_tags", back_populates="tags"
    )