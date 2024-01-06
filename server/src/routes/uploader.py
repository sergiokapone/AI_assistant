import mimetypes
import os

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.extractors import extract_text_from_pdf, extract_text_from_txt
from ..services.auth import auth_service
from ..vector_db.chroma_init import get_chroma_client, initialize_chroma_client

router = APIRouter(prefix="/uploads", tags=["Chat"])


@router.post("/")
async def upload_file(
    current_user: User = Depends(auth_service.get_authenticated_user),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    chroma_helper: initialize_chroma_client = Depends(get_chroma_client),
):
    file_paths = []

    target_folder = "uploads"
    file_path = os.path.join(target_folder, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        file_paths.append(buffer.name)

    # Определяем mime-тип файла
    mime_type, _ = mimetypes.guess_type(file_path)

    # Check mime type and call the appropriate extractor
    match mime_type:
        case "application/pdf":
            await extract_text_from_pdf(
                current_user, file_paths, session, chroma_helper
            )
        case "text/plain":
            await extract_text_from_txt(
                current_user, file_paths, session, chroma_helper
            )
        case _:
            return {"error": "Unsupported file type"}

    return {"file_paths": file_paths}
