from fastapi import APIRouter, HTTPException, UploadFile, status, File
from src.repository.chat import respond
from src.schemas.chat import Response
import pathlib

###router = APIRouter(prefix="/chat", tags=["Comments"])
# @router.post(
#     "/upload",
#     status_code=status.HTTP_201_CREATED,
# )
# async def upload_file(
#     pdf_file: UploadFile,
#     # db: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     return {"file": pdf_file}

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