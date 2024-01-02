from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Answer, Question, User
from ..schemas.chat import Response
from ..services.llmchain import Chain

chain = Chain()


async def respond(current_user: User, session: AsyncSession, instruction: str) -> str:
    question = Question(
        user_id=current_user.id,
        question_text=instruction,
    )

    session.add(question)
    await session.commit()

    response = chain(instruction, current_user.id).lstrip()

    answer = Answer(
        question_id=question.id,
        answer_text=response,
    )

    session.add(answer)
    await session.commit()

    return Response(string=response)
