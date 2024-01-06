import pprint

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import Answer, Question

async def extract_history(user_id: int) -> list:
    session = db_helper.get_scoped_session()
    user_history = []

#    async with session.begin():
    result = await session.execute(
            select(Question, Answer)
            .join(Answer)
            .filter(Question.user_id == user_id)
        )

    for question, answer in result.all():
            user_history.append((question.question_text, answer.answer_text))

    pprint.pprint(type(user_history))
    return user_history
