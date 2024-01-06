from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository import chat as cht
from ..schemas.get_user import Message_History
from ..services.auth import auth_service

router = APIRouter(prefix="/get_history", tags=["Chat"])


@router.get("/", response_model=Message_History)
async def get_history(
    current_user: User = Depends(auth_service.get_authenticated_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    history = await cht.extract_history(current_user, session)
    if history is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not retrive the message history",
        )
    else:
        message_history = Message_History(history=history)
        return message_history
