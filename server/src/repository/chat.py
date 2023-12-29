from sqlalchemy.ext.asyncio import AsyncSession

from src.services.llmchain import Chain

from ..database.models import Answer, Question, User
from ..schemas.chat import Response

API_KEY = "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"

chain = Chain()


async def respond(current_user: User, session: AsyncSession, instruction: str) -> str:
    question = Question(
        user_id=current_user.id,
        question_text=instruction,
    )

    session.add(question)
    await session.commit()

    response = chain(instruction).lstrip()

    answer = Answer(
        question_id=question.id,
        answer_text=response,
    )

    session.add(answer)
    await session.commit()

    return Response(string=response)
