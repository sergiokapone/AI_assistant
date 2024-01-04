from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User


async def cleanup_user_data(current_user: User, user_id):
    async with db_helper.get_session() as session:
        async with session.begin():
            await session.execute(delete(current_user).where(current_user.id == user_id))
            await session.commit()


async def logout_user(session: AsyncSession, current_user: User, user_id):
    async with session.begin():
        await session.execute(delete(current_user).where(current_user.id == user_id))
        await session.commit()
