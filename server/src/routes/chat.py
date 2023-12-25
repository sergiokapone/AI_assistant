from fastapi import APIRouter, UploadFile, status

router = APIRouter(prefix="/chat", tags=["Comments"])


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    pdf_file: UploadFile,
    # db: AsyncSession = Depends(db_helper.session_dependency),
):
    return {"file": pdf_file}
