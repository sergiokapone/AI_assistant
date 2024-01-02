import tempfile
from typing import List, Union
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.database.db_helper import db_helper
from server.src.database.models import User
from server.src.schemas.upload import UploadPDFSchema
from server.src.services.auth import auth_service

router = APIRouter(prefix="/", tags=["Upload PDF file"])
security = HTTPBearer()


@router.post("upload_pdf", response_model=UploadPDFSchema)
async def upload_pdf(
        current_user: User = Depends(auth_service.get_authenticated_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return {current_user, session}
