from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi.security import HTTPBearer

from server.src.schemas.upload import Response

router = APIRouter(prefix="/upload", tags=["Upload PDF file"])
security = HTTPBearer()


@router.post("/", response_model=Response)
async def upload_pdf(files: List[UploadFile] = File(...)):
    pdf_paths = []
