from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from src.schemas.chat import Response
from src.repository.chat import respond

router = APIRouter(prefix='/chat', tags=["chat"])

@router.get("", response_model=Response)
async def read_comments(instruction: str = ''):
    if not instruction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return respond(instruction)