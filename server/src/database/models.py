import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="users")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    question_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    users: Mapped[User] = relationship(back_populates="questions")

    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
    )
    answer_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    question: Mapped[Question] = relationship(back_populates="answers")


class BlacklistToken(Base):
    """
    BlacklistToken Model

    This model represents a blacklisted token in the system, which is used to prevent token reuse.

    :param int id: The unique identifier for the blacklisted token (primary key).
    :param str token: The token string that has been blacklisted (unique and not nullable).
    :param datetime blacklisted_on: The date and time when the token was blacklisted (default is the current time).

    **Example Usage:**

    .. code-block:: python

        blacklisted_token = BlacklistToken(
            token="your_token_string_here"
        )

    """

    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    blacklisted_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
