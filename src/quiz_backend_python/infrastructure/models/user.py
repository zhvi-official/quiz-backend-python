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


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum", create_constraint=True), 
        default=UserRole.PARTICIPANT, 
        server_default=UserRole.PARTICIPANT.value,
        nullable=False
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    quizzes: Mapped[List["Quiz"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    attempts: Mapped[List["QuizAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.username}>"