import os

from fastapi import APIRouter, Depends, File, UploadFile, Path
from fastapi.requests import HTTPConnection
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..database.models import User
from ..repository.extractors import extract_text_from_pdf, extract_text_from_txt, extract_subtitles_from_youtube
from ..services.auth import auth_service
from ..vector_db.chroma_init import get_chroma_client, initialize_chroma_client

router = APIRouter(prefix="/upload", tags=["Upload file"])


@router.post("/pdf")
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

    return {"pdf_paths": pdf_paths}


@router.post("/text")
async def text_from_txt_endpoint(
        current_user: User = Depends(auth_service.get_authenticated_user),
        file: UploadFile = File(...),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        chroma_helper: initialize_chroma_client = Depends(get_chroma_client),
):
    texts_paths = []

    target_folder = "uploads"

    file_path = os.path.join(target_folder, file.filename)
    # Сохраняем загруженный файл
    with open(file_path, 'w') as buffer:
        buffer.write(await buffer.read().decode())
        texts_paths.append(buffer.name)

    # Вызываем функцию извлечения текста из TXT
    text = await extract_text_from_txt(current_user, texts_paths, session, chroma_helper)

    return {"texts_paths": texts_paths}


@router.post("/subtitles")
async def subtitles_from_youtube_endpoint(
        current_user: User = Depends(auth_service.get_authenticated_user),
        # path: UploadFile = Path(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        chroma_helper: initialize_chroma_client = Depends(get_chroma_client),
):
    subtitles_paths = []

    target_folder = "uploads"

    file_path = os.path.join(target_folder, path.filename)


