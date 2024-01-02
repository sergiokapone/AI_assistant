from fastapi import APIRouter, UploadFile, File, Depends, Form

from server.src.schemas.upload import UploadSchema

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/", response_model=UploadSchema)
async def upload_pdf(

        user_query: str = Form(...),
        file: UploadFile = Form(None),
):
    return {"file": file, "user_query": user_query}
