import pathlib

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ..repository.chat import respond
from ..schemas.chat import Response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/", response_model=Response)
async def read_comments(instruction: str = ""):
    if not instruction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return respond(instruction)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}
