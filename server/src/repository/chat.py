from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Answer, Question, User
from ..schemas.chat import Response

API_KEY = "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"

llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2", huggingfacehub_api_token=API_KEY
)
prompt = PromptTemplate(input_variables=["instruction"], template="{instruction}")
llm_chain = LLMChain(llm=llm, prompt=prompt)


async def respond(current_user: User, session: AsyncSession, instruction: str) -> str:
    question = Question(
        user_id=current_user.id,
        question_text=instruction,
    )

    session.add(question)
    await session.commit()

    response = llm_chain.predict(instruction=instruction).lstrip()

    answer = Answer(
        question_id=question.id,
        answer_text=response,
    )

    session.add(answer)
    await session.commit()

    return Response(string=response)
