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


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    
    
    selected_option_ids: Mapped[Optional[List[uuid.UUID]]] = mapped_column(
        ARRAY(Uuid), nullable=True
    )
    text_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    points_awarded: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    attempt: Mapped["QuizAttempt"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="attempt_answers")

    __table_args__ = (
        UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question"),
    )
