from sqlalchemy import select

from ..database.db_helper import db_helper
from ..database.models import Answer, Question


async def extract_history(user_id: int) -> list:
    session = db_helper.get_scoped_session()
    user_history = []

    result = await session.execute(
        select(Question, Answer).join(Answer).filter(Question.user_id == user_id)
    )

    for question, answer in result.all():
        user_history.append((question.question_text, answer.answer_text))

    return user_history
