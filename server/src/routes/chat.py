import pathlib

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.chat import respond
from ..schemas.chat import Response
from ..services.auth import auth_service

router = APIRouter(prefix="/chat", tags=["chat"])



@router.get("/", response_model=Response)
async def read_comments(
    instruction: str = "",
    current_user: User = Depends(auth_service.get_authenticated_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not instruction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return await respond(current_user, session=session, instruction=instruction)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}
