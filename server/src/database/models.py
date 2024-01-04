import datetime
import os
import sys

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Получаем путь к текущему файлу (models.py)
current_file = os.path.realpath(__file__)

# Определяем, вызывается ли код из Alembic (по наличию alembic в sys.argv)
is_alembic = "alembic" in sys.argv[0]

# Импортируем необходимые модули
if is_alembic:
    from config.llm_list import LLMNameEnum  # Используем абсолютный импорт
else:
    from ..config.llm_list import LLMNameEnum  # Используем относительный импорт


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_llm: Mapped[str] = mapped_column(
        String(255), nullable=False, default=LLMNameEnum.llm_option1
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    user_questions: Mapped[list["Question"]] = relationship(back_populates="user")
    user_uploaded_texts: Mapped[list["UploadedText"]] = relationship(
        back_populates="user"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    question_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped[User] = relationship(back_populates="user_questions")
    answers: Mapped["Answer"] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
    )
    answer_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    question: Mapped[Question] = relationship(back_populates="answers")


class UploadedText(Base):
    __tablename__ = "uploaded_text"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    uploaded_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped[User] = relationship(back_populates="user_uploaded_texts")


class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    blacklisted_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
