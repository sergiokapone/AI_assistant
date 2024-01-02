import tempfile
from typing import List, Union
from fastapi import APIRouter, UploadFile, File, Depends, Form

from sqlalchemy.ext.asyncio import AsyncSession
from server.src.database.models import User
from server.src.schemas.upload import UploadSchema
from server.src.services.auth import auth_service

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/", response_model=UploadSchema)
async def upload_pdf(
        current_user: User = Depends(auth_service.get_authenticated_user),
        user_query: str = Form(...),
        file: UploadFile = Form(None),
):
    return {"user": current_user, "file": file, "user_query": user_query}
