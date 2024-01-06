import os

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.extractors import extract_text_from_pdf
from ..services.auth import auth_service
from ..vector_db.chroma_init import get_chroma_client, initialize_chroma_client

from ..services.llmchain import chain

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/")
async def upload_pdf(
    current_user: User = Depends(auth_service.get_authenticated_user),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    chroma_helper: initialize_chroma_client = Depends(get_chroma_client),
):
    pdf_paths = []

    target_folder = "uploads"

    file_path = os.path.join(target_folder, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        pdf_paths.append(buffer.name)

    await extract_text_from_pdf(current_user, pdf_paths, session, chroma_helper)

    await chain.update(current_user.id)

    return {"pdf_paths": pdf_paths}
