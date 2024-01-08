from sqlalchemy import select

from ..database.db_helper import db_helper
from ..database.models import Answer, Question, User


async def extract_history(user_id: int) -> list:
    session = db_helper.get_scoped_session()
    user_history = []

    result = await session.execute(
        select(Question, Answer).join(Answer).filter(Question.user_id == user_id)
    )

    for question, answer in result.all():
        user_history.append((question.question_text, answer.answer_text))
    
    session.close()

    await session.close()

    return user_history


async def get_selected_llm(user_id: int) -> str:
    session = db_helper.get_scoped_session()
    user = await session.get(User, user_id)
    session.close()
    return user.selected_llm
