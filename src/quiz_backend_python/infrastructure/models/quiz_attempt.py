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


class QuizAttempt(TimestampMixin, Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    status: Mapped[AttemptStatus] = mapped_column(
        Enum(AttemptStatus, name="attempt_status_enum"), 
        default=AttemptStatus.IN_PROGRESS,
        nullable=False
    )
    
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_sec: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


    quiz: Mapped["Quiz"] = relationship(back_populates="attempts")
    user: Mapped["User"] = relationship(back_populates="attempts")
    answers: Mapped[List["AttemptAnswer"]] = relationship(
        back_populates="attempt", 
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_attempts_user_started", "user_id", "started_at"),
        Index("ix_attempts_quiz_score", "quiz_id", "score"),
    )
