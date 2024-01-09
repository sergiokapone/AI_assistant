from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import User
from ..services.llmchain import chain


async def llm_selector(
    llm_name: str,
    current_user: User,
    session: AsyncSession,
) -> None:
    smtp = update(User).where(User.id == current_user.id).values(selected_llm=llm_name)
    await session.execute(smtp)
    await session.commit()
    await chain.update(current_user.id)
