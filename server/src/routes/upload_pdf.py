from fastapi import APIRouter, UploadFile, File, Depends, Form

router = APIRouter(prefix="/upload_pdf", tags=["Upload file"])


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_paths = []

    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
        pdf_paths.append(buffer.name)

    return {"pdf_paths": pdf_paths}
