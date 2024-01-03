from fastapi import APIRouter, Depends, File, UploadFile

from server.src.database.models import User
from server.src.repository import extract_text_from_pdf

from ..services import auth_service

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/")
async def upload_pdf(
    current_user: User = Depends(auth_service.get_authenticated_user),
    file: UploadFile = File(...),
):
    pdf_paths = []

    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
        pdf_paths.append(buffer.name)

    extract_text_from_pdf(current_user.id, pdf_paths)

    return {"pdf_paths": pdf_paths}
