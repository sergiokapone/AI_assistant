import pprint

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Answer, Question, User
from ..schemas.chat import Response
from ..services.llmchain import chain


async def respond(current_user: User, session: AsyncSession, instruction: str) -> str:
    question = Question(
        user_id=current_user.id,
        question_text=instruction,
    )

    session.add(question)
    await session.commit()

    response = await chain(instruction, current_user.id)


    answer = Answer(
        question_id=question.id,
        answer_text=response,
    )

    session.add(answer)
    await session.commit()

    #history = await extract_history(current_user, session)
    #pprint.pprint(history)

    return Response(string=response)