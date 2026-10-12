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


class Quiz(TimestampMixin, Base):
    __tablename__ = "quizzes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cover_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    difficulty: Mapped[Optional[QuizDifficulty]] = mapped_column(
        Enum(QuizDifficulty, name="quiz_difficulty_enum"), nullable=True
    )
    status: Mapped[QuizStatus] = mapped_column(
        Enum(QuizStatus, name="quiz_status_enum"), 
        default=QuizStatus.DRAFT, 
        server_default=QuizStatus.DRAFT.value,
        nullable=False
    )
    
    time_limit_sec: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_attempts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shuffle_questions: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)


    author: Mapped["User"] = relationship(back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(
        back_populates="quiz", 
        cascade="all, delete-orphan", 
        order_by="Question.order_index"
    )
    attempts: Mapped[List["QuizAttempt"]] = relationship(back_populates="quiz", cascade="all, delete-orphan")
    
    
    tags: Mapped[List["Tag"]] = relationship(
        secondary="quiz_tags", back_populates="quizzes"
    )

    __table_args__ = (
        Index("ix_quizzes_author_id", "author_id"),
        Index("ix_quizzes_status_category", "status", "category"),
        Index("ix_quizzes_created_at_desc", "created_at"), 
    )

    def __repr__(self) -> str:
        return f"<Quiz {self.title}>"