import logging
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from ..database.models import BlacklistToken, User
from ..schemas.users import UserSchema
from ..services.llmchain import chain


async def create_user(body: UserSchema, session: AsyncSession) -> User:
    new_user = User(**body.model_dump())

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        await session.rollback()
        raise e


async def remove_user(current_user: User, session: AsyncSession):
    try:
        # Downloading a user from the database using the current session
        user_to_remove = await session.get(User, current_user.id)

        if user_to_remove:
            await session.delete(user_to_remove)
            await session.commit()
            chain.delete_chain(current_user.id)
        else:
            logging.error("User not found in the session.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
    except IntegrityError as e:
        # IntegrityError может возникнуть, если есть ссылки на пользователя в других таблицах
        logging.error(f"Error removing user: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing user",
        )
    except Exception as e:
        logging.error(f"Error removing user: {e}")
        await session.rollback()
        raise e


async def get_users(skip: int, limit: int, db: AsyncSession) -> list[User]:
    """
    The get_users function returns a list of all users from the database.

    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of results returned
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of all users
    """
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.

    :param email: str: Get the email from the user
    :param db: Session: Pass a database session to the function
    :return: A user object if the email is found in the database
    """
    try:
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        return user
    except NoResultFound:
        return None


async def get_user_by_user_id(user_id: int, db: AsyncSession) -> User | None:
    """
    Get User by User ID

    This function retrieves a user by their user ID from the database.

    :param int user_id: The ID of the user to retrieve.
    :param AsyncSession db: An asynchronous database session.
    :return: The user with the specified ID, or None if the user is not found.
    :rtype: User | None
    """

    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return user
    except NoResultFound:
        return None


async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session, then returns the user with that email.

    :param email: str: Get the email from the user
    :param db: Session: Pass a database session to the function
    :return: A user object if the email is found in the database
    """
    try:
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        return user
    except NoResultFound:
        return None


#### BLACKLIST #####


async def add_to_blacklist(token: str, db: AsyncSession) -> None:
    """
    **Adds a token to the blacklist.**

    :param token: str: Pass the token to be blacklisted
    :param db: AsyncSession: Create a new session with the database
    :return: None
    """
    blacklist_token = BlacklistToken(token=token, blacklisted_on=datetime.now())

    try:
        db.add(blacklist_token)
        await db.commit()
        await db.refresh(blacklist_token)
    except Exception as e:
        await db.rollback()
        raise e


async def is_blacklisted_token(token: str, db: AsyncSession) -> bool:
    """
    Check if a Token is Blacklisted

    This function checks if a given token is blacklisted in the database.

    :param str token: The token to be checked.
    :param AsyncSession db: An asynchronous database session.
    :return: True if the token is blacklisted, False otherwise.
    :rtype: bool
    """

    result = await db.execute(
        select(BlacklistToken).filter(BlacklistToken.token == token)
    )

    blacklist_token = result.scalar_one_or_none()

    if blacklist_token:
        return True
    return False
