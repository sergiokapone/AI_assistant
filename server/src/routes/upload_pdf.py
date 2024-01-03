from fastapi import APIRouter, UploadFile, File, Depends, Form

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/")
async def upload_pdf(
        file: UploadFile = Form(None),
):
    return {"file": file}
