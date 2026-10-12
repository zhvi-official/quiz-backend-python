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



class Question(TimestampMixin, Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    
    type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type_enum"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    
    text_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True) 
    
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    options: Mapped[List["QuestionOption"]] = relationship(
        back_populates="question", 
        cascade="all, delete-orphan", 
        order_by="QuestionOption.order_index"
    )
    attempt_answers: Mapped[List["AttemptAnswer"]] = relationship(back_populates="question")

    __table_args__ = (
        Index("ix_questions_quiz_order", "quiz_id", "order_index"),
    )